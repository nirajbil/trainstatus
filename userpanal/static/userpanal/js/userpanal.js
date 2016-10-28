/**
 * Created by Niraj on 10/10/2016.
 */


$(document).on('submit','#pnrstatus', function (e) {
    var pnrno = $('#pnrno').val();

    if(isNaN(pnrno) || pnrno.length != 10){
        alert('PNR Number Should be 10 Digit');
        return false;
    }

    e.preventDefault();


    $.ajax({
        type : 'POST',
        url : '/get_pnr_status/',

        data : {
            pnrno: $('#pnrno').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },



        success: function (data) {
            console.log(data.response_code);

            if (data.response_code == 200) {
                $('#pnr_status_html').html(get_pnr_status_html(data));

            }
            else {
                alert(data.response_code);
            }
        },


        failure: function () {
            alert('Got an error dude');
        },

    })



    function get_pnr_status_html(data){
        var httpresonce="";
        httpresonce += '<div class="container-fluid">';
        httpresonce += '   <h4>PNR - ' +  data.pnr + '</h4>';
        httpresonce += '<table class="table table-sm table-reflow" style="height:20px;font-size:12px">';
        httpresonce += '    <td>';

        httpresonce += '       <table class="table table-bordered table-sm " >';
        httpresonce += '           <tbody>';
        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Train Name:</th>';
        httpresonce += '                 <td>' + data.train_name + '</td>';
        httpresonce += '               </tr>';
        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Train Number:</th>';
        httpresonce += '                 <td>' +  data.train_num + '</td>';
        httpresonce += '               </tr>';
        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">From Station:</th>';
        httpresonce += '                 <td>' + data.from_station.name + ' (' + data.from_station.code + ')' + '</td>';
        httpresonce += '               </tr>';

        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">To Station:</th>';
        httpresonce += '                 <td>' + data.to_station.name + ' (' + data.to_station.code + ')' + '</td>';
        httpresonce += '               </tr>';

        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Class:</th>';
        httpresonce += '                 <td>' + data.train_class + '</td>';
        httpresonce += '               </tr>';
        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Date Of Journey:</th>';
        httpresonce += '                 <td>' + data.doj + '</td>';
        httpresonce += '               </tr>';

        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Reserved Upto:</th>';
        httpresonce += '                 <td>' + data.reservation_upto.name + ' (' + data.reservation_upto.code + ')' + '</td>';
        httpresonce += '               </tr>';

        httpresonce += '               <tr>';
        httpresonce += '                 <th scope="row">Boarding Point:</th>';
        httpresonce += '                 <td>' + data.boarding_point.name + ' (' + data.boarding_point.code + ')' + '</td>';
        httpresonce += '               </tr>';
        httpresonce += '           </tbody>';
        httpresonce += '       </table>';

        httpresonce += '        </td>';
        httpresonce += '        <td>';

        httpresonce += '       <table class="table table-bordered table-sm ">';
        httpresonce += '         <thead>';
        httpresonce += '           <tr>';
        httpresonce += '             <th>Sr.No</th>';
        httpresonce += '             <th>Booking Status</th>';
        httpresonce += '             <th>Current Status</th>';
        httpresonce += '           </tr>';
        httpresonce += '         </thead>';
        httpresonce += '         <tbody>';

                $.each(data.passengers, function () {
        httpresonce += '           <tr>';
        httpresonce += '             <th scope="row">Pasenger ' +  this.no + '</th>';
        httpresonce += '             <td>' + this.booking_status + '</td>';
        httpresonce += '             <td>' + this.current_status + '</td>';
        httpresonce += '           </tr>';
                });


        httpresonce += '           <tr>';
        httpresonce += '             <th scope="row">Charting Status</th>';
                      if (data.chart_prepared == 'N'){
        httpresonce += '               <td colspan="3">CHART NOT PREPARED</td>';
                      }
                      else{
        httpresonce += '               <td colspan="3">CHART PREPARED</td>';
                      }

        httpresonce += '           </tr>';
        httpresonce += '         </tbody>';
        httpresonce += '       </table>';
        httpresonce += '    </td>';
        httpresonce += '</table>';


        httpresonce += '</div>';

        return httpresonce;
    }

});
