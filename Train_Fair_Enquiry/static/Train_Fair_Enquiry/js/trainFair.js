/**
 * Created by Niraj on 10/12/2016.
 */

$(document).on('submit','#train_fair', function (e) {
    var source = $('#source').val();
    if(source.length == 0){
        alert('Please Enter Source Station');
        return false;
    }

    var dest = $('#dest').val();
    if(dest.length == 0){
        alert('Please Enter Destination Station');
        return false;
    }

    var date = $('#date').val();
    if(date.length == 0){
        alert('Please Enter Date Of Journey');
        return false;
    }

    var Passenger_Age = $('#Passenger_Age').val();
    if(Passenger_Age.length == 0){
        alert('Please Enter Passenger Age');
        return false;
    }

   /* alert('*********** correct ************');            isNaN(pnrno) ||  */



    e.preventDefault();
    $.ajax({
        type: 'POST',
        url : '/train_fair/',
        data:{
            source:$('#source').val(),
            dest:$('#dest').val(),
            date:$('#date').val(),
            train_quota:$('#train_quota').val(),
            Passenger_Age:$('#Passenger_Age').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){

            console.log(data.response_code);
            if(data.response_code == 200)
            {
                $('#output').html(trainAvailable(data));
            }
            else
            {
                alert(data.response_code);
            }
        },
        failure: function() {
                alert('Got an error dude');
        },

    })

    function trainAvailable(data){
        var httpresponce="";

        httpresponce += '<table class="table table-bordered" id="myTable">';
        httpresponce += '  <thead>';
        httpresponce += '    <tr>';
        httpresponce += '      <th>Train No</th>';
        httpresponce += '      <th>Train Name</th>';
        httpresponce += '      <th>From Station</th>';
        httpresponce += '      <th>Departure Time</th>';
        httpresponce += '      <th>To Station</th>';
        httpresponce += '      <th>Arrival Time</th>';
        httpresponce += '      <th>Travel Time</th>';
        httpresponce += '      <th>Running Days</th>';
        httpresponce += '      <th>classes Available</th>';
        httpresponce += '    </tr>';
        httpresponce += '  </thead>';
        httpresponce += '  <tbody>';

        for(i=0;i<data.train.length;i++)
        {
            console.log(data.train[i].number);
            httpresponce += '<td>';
            /*httpresponce += '<td id="number-' + i + '">' + data.train[i].number + '</td>';*/
            httpresponce += '<a href="#" class="collectionlist" name="'+ data.train[i].number +'" id="' + i + '">' + data.train[i].number + '</a>';
            httpresponce += '</td>';

            console.log(data.train[i].name);
            httpresponce += '<td id="tname-' + i + '">' + data.train[i].name + '</td>';

            console.log(data.train[i].from);
            httpresponce += '<td id="from_name-' + i + '">' + data.train[i].from.name+ ' - ' + data.train[i].from.code + '</td>';

            console.log(data.train[i].src_departure_time);
            httpresponce += '<td id="src_departure_time-' + i + '">' + data.train[i].src_departure_time + '</td>';

            console.log(data.train[i].to);
            httpresponce += '<td id="to_name-' + i + '">' + data.train[i].to.name + ' - ' + data.train[i].to.code + '</td>';

            console.log(data.train[i].dest_arrival_time);
            httpresponce += '<td id="dest_arrival_time-' + i + '">' + data.train[i].dest_arrival_time + '</td>';

            console.log(data.train[i].travel_time);
            httpresponce += '<td id="travel_time-' + i + '">' + data.train[i].travel_time + '</td>';

            httpresponce += '<td>';
            $.each(data.train[i].days, function () {
                if(this.runs == 'Y')
                {
                    console.log(this.day_code);
                    httpresponce += this.day_code + ' ';
                }
                /*console.log(this.runs);console.log(this.day_code);*/
            });
            httpresponce += '</td>';

            httpresponce += '<td>';
            $.each(data.train[i].classes, function () {
                if(this.available == 'Y')
                {
                    console.log(this.class_code);
                    /*httpresponce += '<a href="#" class="collectionlist" name="'+ this.class_code +'" id="' + i + '">' + this.class_code + '</a>' +' ';*/
                    httpresponce += this.class_code + ' ';
                }
                /*console.log(this.available);console.log(this.class_code);*/
            });
            httpresponce += '</td>';
            httpresponce += '</tr>';
        }

          httpresponce += '</tbody></table>';
        return httpresponce;
    }
});

$(document).on('click', '.collectionlist', function(e){
    var id = $(this).attr('id');
    var name = $(this).attr('name');

    var tname;
    var from_name;
    var to_name;


    var test = $("#myTable tbody").each(function() {
         /*number = $(this).find('#number-'+id).text();*/
         tname = $(this).find('#tname-'+id).text();
         from_name = $(this).find('#from_name-'+id).text();
         to_name = $(this).find('#to_name-'+id).text();


     });



    console.log(to_name);
    console.log(from_name);
    console.log(id);
    console.log(name);

    e.preventDefault();
    $.ajax({
        type: 'POST',
        url : '/train_fair_detail/',
        data:{
            'from_name':from_name,
            'to_name':to_name,
            'train_number':name,
            date:$('#date').val(),
            train_quota:$('#train_quota').val(),
            Passenger_Age:$('#Passenger_Age').val(),

            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){
                if(data.response_code == 200)
                {
                    $('#trainFairDetail').html(trainFairDetail(data));
                }
                else
                {
                    alert(data.response_code);
                }

        },
        failure: function() {
                alert('Got an error dude');
        },

    })

    function trainFairDetail(data)
    {
        var httpresonce="";

        httpresonce+='        <table class="table table-bordered" id="myTable">';
        httpresonce+='          <thead>';
        httpresonce+='            <tr>';
        httpresonce+='              <th colspan="4">Train : ' + data.train.name + '  (' +  data.train.number + ')' + '</th>';
        httpresonce+='            </tr>';
        httpresonce+='            <tr>';
        httpresonce+='              <th colspan="1">Code </th>';
        httpresonce+='              <th colspan="1">Name</th>';
        httpresonce+='              <th colspan="1">Fare</th>';
        httpresonce+='            </tr>';
        httpresonce+='          </thead>';
        httpresonce+='          <tbody>';
        $.each(data.fare, function () {
            httpresonce+='                    <tr>';
            httpresonce+='                    <td>' + this.code + '</td>';
            httpresonce+='                    <td>' + this.name + '</td>';
            httpresonce+='                    <td>'+ this.fare + '</td>';
            httpresonce+='                    </tr>';
        });
        httpresonce+='          </tbody>';
        httpresonce+='        </table>';
        httpresonce+='    </div>';

        return httpresonce;
    }
});

