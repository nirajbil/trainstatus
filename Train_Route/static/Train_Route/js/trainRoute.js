/**
 * Created by Niraj on 10/14/2016.
 */

require(["jquery","jquery-mloading"],function($){
    $("#trainRoute").click(function(e) {
        var trainNumber = $('#trainNumber').val();

        if(isNaN(trainNumber) || trainNumber.length != 5){
            alert('Train Number Should be Digit');
            return false;
        }

        //alert('*********** correct trainRoute ************');

        e.preventDefault();
        $("body").mLoading();

        $.ajax({
            type: 'POST',
            url : '/train_Route_detail/',
            data:{
                trainNumber:$('#trainNumber').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },

            success:function(data){
                console.log(data.response_code);
                if(data.response_code == 200)
                {
                    $('#train_Route_html').html(trainRoute(data));
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

        function trainRoute(data){
            /*alert(data.response_code);*/
            var httpresonce="";
        httpresonce += '<table class="table table-bordered" id="myTable">';
        httpresonce += '<thead>';
        httpresonce += ' <tr>';
        httpresonce += ' <th>No</th>';
        httpresonce += '<th>Station Code</th>';
        httpresonce += '      <th>Station Name</th>';
        httpresonce += '      <th>Arrival</th>';
        httpresonce += '      <th>Departure</th>';
        httpresonce += '      <th>Day</th>';
        httpresonce += '      <th>Route</th>';
        httpresonce += '      <th>Halt</th>';
        httpresonce += '      <th>Distance</th>';
        httpresonce += '      <th>State</th>';
        httpresonce += '    </tr>';
        httpresonce += '  </thead>';
        httpresonce += '  <tbody>';

        $.each(data.train_route, function () {
                httpresonce += '    <tr>';
                httpresonce += '      <th scope="row">' + this.no + '</th>';
                httpresonce += '      <td>' + this.code + '</td>';
                httpresonce += '      <td>' + this.fullname + '</td>';
                httpresonce += '      <td>' + this.scharr + '</td>';
                httpresonce += '      <td>' + this.schdep + '</td>';
                httpresonce += '      <td>' + this.day + '</td>';
                httpresonce += '      <td>' + this.route + '</td>';
                httpresonce += '      <td>' + this.halt + 'min</td>';
                httpresonce += '      <td>' + this.distance + '</td>';
                httpresonce += '      <td>' + this.state + '</td>';
                httpresonce += '    </tr>';
        });


        httpresonce += '  </tbody>';
            return httpresonce;
        }
    });
});
