/**
 * Created by Niraj on 10/12/2016.
 */

require(["jquery","jquery-mloading"],function($){
    $("#train_between_station").click(function(e) {
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

        e.preventDefault();
        $("body").mLoading();
        $.ajax({
            type: 'POST',
            url : '/find_train/',
            data:{
                source:$('#source').val(),
                dest:$('#dest').val(),
                date:$('#date').val(),
                train_quota:$('#train_quota').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(data){

                console.log(data.response_code);
                if(data.response_code == 200)
                {
                    if(data.total == 0){
                        $('#output').html('<div class="alert alert-info"><strong>No Trains Are Available On This Date.</strong></div>');
                    }
                    else{
                        $('#output').html(trainAvailable(data));
                    }
                }
                else
                {
                    alert(data.response_code);
                }
                setTimeout(function(){ $("body").mLoading('hide'); }, 10);

                /*
                $.post('Train_Between_Stations/trainBetweenStations.html' ,
                        {
                            person_name : 'Niraj',
                        } ,
                        function(data){
                            $('#output').html(data);
                        }

                    );
                */
                /*
                $.each(data,function(key, value){
                    $('ul').append("<li>" + value.train_number + "<li>");
                });
                */
                /*
                alert(data.response_code);
                */
                /*
                $('.ajaxprogress').hide();
                */
               /* $('output').html("<h1> niraj</h1>");*/

            },
            failure: function() {
                    alert('Got an error dude');
            },

        })

        function trainAvailable(data){
            /*alert(data.response_code);*/
            var httpresonce="";
        httpresonce = '\
        <table class="table table-bordered" id="myTable">\
          <thead>   \
            <tr>    \
              <th>Train No</th> \
              <th>Train Name</th> \
              <th>From Station</th> \
              <th>Departure Time</th> \
              <th>To Station</th> \
              <th>Arrival Time</th> \
              <th>Travel Time</th> \
              <th>Running Days</th> \
              <th>classes Available</th> \
            </tr> \
          </thead> \
          <tbody>';



            for(i=0;i<data.train.length;i++)
            {
                console.log(data.train[i].number);
                httpresonce += '<td id="number-' + i + '">' + data.train[i].number + '</td>';

                console.log(data.train[i].name);
                httpresonce += '<td id="tname-' + i + '">' + data.train[i].name + '</td>';

                console.log(data.train[i].from);
                httpresonce += '<td id="from_name-' + i + '">' + data.train[i].from.name+ ' - ' + data.train[i].from.code + '</td>';

                console.log(data.train[i].src_departure_time);
                httpresonce += '<td id="src_departure_time-' + i + '">' + data.train[i].src_departure_time + '</td>';

                console.log(data.train[i].to);
                httpresonce += '<td id="to_name-' + i + '">' + data.train[i].to.name + ' - ' + data.train[i].to.code + '</td>';

                console.log(data.train[i].dest_arrival_time);
                httpresonce += '<td id="dest_arrival_time-' + i + '">' + data.train[i].dest_arrival_time + '</td>';

                console.log(data.train[i].travel_time);
                httpresonce += '<td id="travel_time-' + i + '">' + data.train[i].travel_time + '</td>';

                httpresonce += '<td>';
                $.each(data.train[i].days, function () {
                    if(this.runs == 'Y')
                    {
                        console.log(this.day_code);
                        httpresonce += this.day_code + ' ';
                    }
                    /*console.log(this.runs);console.log(this.day_code);*/
                });
                httpresonce += '</td>';

                httpresonce += '<td>';
                $.each(data.train[i].classes, function () {
                    if(this.available == 'Y')
                    {
                        console.log(this.class_code);
                        httpresonce += '<a href="#" class="trainClassList" name="'+ this.class_code +'" id="' + i + '">' + this.class_code + '</a>' +' ';

                    }
                    /*console.log(this.available);console.log(this.class_code);*/
                });
                httpresonce += '</td>';
                httpresonce += '</tr>';
            }

              httpresonce += '</tbody></table>';



            return httpresonce;
        }
    });
});


require(["jquery","jquery-mloading"],function($){
$(document).on('click', '.trainClassList', function(e){
    var id = $(this).attr('id');
    var name = $(this).attr('name');
    var number;
    var tname;
    var from_name;
    var to_name;


    var test = $("#myTable tbody").each(function() {
         number = $(this).find('#number-'+id).text();
         tname = $(this).find('#tname-'+id).text();
         from_name = $(this).find('#from_name-'+id).text();
         to_name = $(this).find('#to_name-'+id).text();


     });


    console.log(number);
    console.log(to_name);
    console.log(from_name);
    console.log(id);
    console.log(name);

    e.preventDefault();
    $("body").mLoading();
    $.ajax({
        type: 'POST',
        url : '/find_seat/',
        data:{
            'from_name':from_name,
            'to_name':to_name,
            'train_class':name,
            date:$('#date').val(),
            train_quota:$('#train_quota').val(),
            'number':number,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){
                if(data.response_code == 200)
                {
                    $('#seatAvailableoutput').html(seatAvailable(data));
                }
                else
                {
                    alert(data.error);
                }
                setTimeout(function(){ $("body").mLoading('hide'); }, 10);
        },
        failure: function() {
                alert('Got an error dude');
        },

    })

    function seatAvailable(data)
    {
        var httpresonce="";

        httpresonce+= '    <table class="table table-bordered" id="myTable2" >';
        httpresonce+= '      <thead>';
        httpresonce+= '        <tr>';
        httpresonce+= '          <th>Train Number</th>';
        httpresonce+= '          <th>Train Name</th>';
        httpresonce+= '          <th>Date</th>';
        httpresonce+= '          <th>Source Station</th>';
        httpresonce+= '          <th>Destination Station</th>';
        httpresonce+= '          <th>Quota Code</th>';
        httpresonce+= '        </tr>';
        httpresonce+= '      </thead>';
        httpresonce+= '      <tbody>';
        httpresonce+= '        <tr>';
        httpresonce+= '         <td>' +  data.train_number + '</td>';
        httpresonce+= '          <td>' +  data.train_name  + '</td>';
        httpresonce+= '          <td>' +  data.last_updated.date  +'</td>';
        httpresonce+= '          <td>' +  data.from_station.name + '(' + data.from_station.code + ')'+ '</td>';
        httpresonce+= '          <td>' +  data.to_station.name + '(' +  data.to_station.code + ')' + '</td>';
        httpresonce+= '          <td>' +  data.quota.quota_name + '(' + data.quota.quota_code + ')' + '</td>';
        httpresonce+= '        </tr>';
        httpresonce+= '      </tbody>';
        httpresonce+= '    </table>';

        httpresonce+= '    <table class="table table-bordered"  id="myTable2" >';
        httpresonce+= '      <thead>';
        httpresonce+= '        <tr>';
        httpresonce+= '          <th>No</th>';
        httpresonce+= '          <th>Date (DD-MM-YYYY)</th>';
        httpresonce+= '          <th>Class - ' +  data.train_class.class_name +  '(' + data.train_class.class_code + ')' + '</th>'
        httpresonce+= '        </tr>';
        httpresonce+= '      </thead>';
        httpresonce+= '      <tbody>';


                for(i=0;i<data.availability.length;i++){
        httpresonce+= '            <tr>';
        httpresonce+= '              <th scope="row">' + (i+1) + '</th>';
        httpresonce+= '              <td>' +  data.availability[i].date  + '</td>';
        httpresonce+= '              <td>' +  data.availability[i].status + '</td>';
        httpresonce+= '            </tr>';
                }
        httpresonce+= '      </tbody>';
        httpresonce+= '    </table>';



        return httpresonce;
    }

});
});

