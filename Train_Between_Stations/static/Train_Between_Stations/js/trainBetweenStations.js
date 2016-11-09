/**
 * Created by Niraj on 10/14/2016.
 */

require(["jquery","jquery-mloading"],function($){
    $("#train_station").click(function(e) {
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
            url : '/train_between/',
            data:{
                source:$('#source').val(),
                dest:$('#dest').val(),
                date:$('#date').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(data){
                console.log(data.response_code);
                if(data.response_code == 200)
                {
                    if(data.total == 0){
                        $('#train_station_output').html('<div class="alert alert-info"><strong>No Trains Are Available On This Date.</strong></div>');
                    }
                    else{
                        $('#train_station_output').html(trainAvailable(data));
                    }

                }
                else
                {
                    alert(data.response_code);
                }
                setTimeout(function(){ $("body").mLoading('hide'); }, 10);
            },
            failure: function() {
                    alert('Got an error dude');
            },

        })

        function trainAvailable(data){
            /*alert(data.response_code);*/
            var httpresonce="";

            httpresonce += '<table class="table table-bordered table-sm " id="myTable">';
            httpresonce += '<thead>';
            httpresonce += ' <tr>';
            httpresonce += ' <th>Train No</th>';
            httpresonce += '<th>Train Name</th>';
            httpresonce += '      <th>From Station</th>';
            httpresonce += '      <th>Departure Time</th>';
            httpresonce += '      <th>To Station</th>';
            httpresonce += '      <th>Arrival Time</th>';
            httpresonce += '      <th>Travel Time</th>';
            httpresonce += '      <th>Running Days</th>';
            httpresonce += '      <th>classes Available</th>';
            httpresonce += '    </tr>';
            httpresonce += '  </thead>';
            httpresonce += '  <tbody>';


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




