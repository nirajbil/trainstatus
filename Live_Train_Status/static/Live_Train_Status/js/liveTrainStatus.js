/**
 * Created by Niraj on 10/10/2016.
 */
$(document).on('submit','#livetrainstatus', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url : '/live_train_status_detail/',
        data:{
            trainNumber:$('#trainNumber').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){

            console.log(data.response_code);
            if(data.response_code == 200)
            {

                $('#live_train_status_html').html(liveTrainStatus(data));
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

    function liveTrainStatus(data){
        /*alert(data.response_code);*/
        var httpresonce="";
        /*httpresonce += '<div class="container">';*/

        httpresonce += '<table class="table table-bordered" id="myTable">';

        httpresonce += '  <thead>';
        httpresonce += '    <tr>';
        httpresonce += '      <th colspan="5"><h5>Train : ' + data.train_number + '</h5></th>';
        httpresonce += '      <th colspan="5"><h5>Start Date: ' + data.start_date + '</h5></th>';
        httpresonce += '    </tr>';

        httpresonce += '    <tr>';
        httpresonce += '      <th colspan="10"><h5>' +  data.position + '</h5></th>';
        httpresonce += '    </tr>';

        httpresonce += '    <tr>';
        /*httpresonce += '      <th>No</th>';*/
        httpresonce += '      <th>Station Name</th>';
        httpresonce += '      <th>Station code</th>';
        httpresonce += '      <th>Sch. Arrival</th>';
        httpresonce += '      <th>Sch. Departure</th>';
        httpresonce += '      <th>Actual Arrival</th>';
        httpresonce += '      <th>Actual Departure</th>';
        httpresonce += '      <th>Late min</th>';
        httpresonce += '      <th>Distance</th>';

        httpresonce += '    </tr>';
        httpresonce += '  </thead>';
        httpresonce += '  <tbody>';

        $.each(data.route, function () {

          if(this.no == 1 && data.current_station.no==1){
              if(this.no == 1){
                  httpresonce += '        <tr  class="blinkYellow">';
                  /*httpresonce += '          <th scope="row">' + this.no + '</th>';*/
                  httpresonce += '          <td>' + this.station_.name + '</td>';
                  httpresonce += '          <td>' + this.station_.code + '</td>';
                  httpresonce += '          <td>' + this.scharr + '</td>';
                  httpresonce += '          <td>' + this.schdep + '</td>';
                  httpresonce += '          <td>' + this.actarr + '</td>';
                  httpresonce += '          <td>' + this.actdep + '</td>';
                  httpresonce += '          <td>' + this.latemin + '</td>';
                  httpresonce += '          <td>' + this.distance + '</td>';
                  httpresonce += '        </tr>';
              }
              else{
                  httpresonce += '        <tr>';
                  /*httpresonce += '          <th scope="row">' + this.no + '</th>';*/
                  httpresonce += '          <td>' + this.station_.name + '</td>';
                  httpresonce += '          <td>' + this.station_.code + '</td>';
                  httpresonce += '          <td>' + this.scharr + '</td>';
                  httpresonce += '          <td>' + this.schdep + '</td>';
                  httpresonce += '          <td>' + this.actarr + '</td>';
                  httpresonce += '          <td>' + this.actdep + '</td>';
                  httpresonce += '          <td>' + this.latemin + '</td>';
                  httpresonce += '          <td>' + this.distance + '</td>';
                  httpresonce += '        </tr>';
              }
          }
          else {
              if (this.no == data.current_station.no) {
                  httpresonce += '        <tr  class="blinkYellow">';
                  /*httpresonce += '          <th scope="row">' + this.no + '</th>';*/
                  httpresonce += '          <td>' + data.current_station.station_.name + '</td>';
                  httpresonce += '          <td>' + data.current_station.station_.code + '</td>';
                  httpresonce += '          <td>' + data.current_station.scharr + '</td>';
                  httpresonce += '          <td>' + data.current_station.schdep + '</td>';
                  httpresonce += '          <td>' + data.current_station.actarr + '</td>';
                  httpresonce += '          <td>' + data.current_station.actdep + '</td>';
                  httpresonce += '          <td>' + data.current_station.latemin + '</td>';
                  httpresonce += '          <td>' + data.current_station.distance + '</td>';
                  httpresonce += '        </tr>';
              }
              {
                  httpresonce += '        <tr>';
                  /*httpresonce += '          <th scope="row">' + this.no + '</th>';*/
                  httpresonce += '          <td>' + this.station_.name + '</td>';
                  httpresonce += '          <td>' + this.station_.code + '</td>';
                  httpresonce += '          <td>' + this.scharr + '</td>';
                  httpresonce += '          <td>' + this.schdep + '</td>';
                  httpresonce += '          <td>' + this.actarr + '</td>';
                  httpresonce += '          <td>' + this.actdep + '</td>';
                  httpresonce += '          <td>' + this.latemin + '</td>';
                  httpresonce += '          <td>' + this.distance + '</td>';
                  httpresonce += '        </tr>';
              }
          }

          });


        httpresonce += '  </tbody>';
        httpresonce += '</table>';
        /*httpresonce += '</div>';*/


        return httpresonce;
    }
});
