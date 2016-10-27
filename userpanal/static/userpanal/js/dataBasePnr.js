/**
 * Created by Niraj on 10/26/2016.
 */


function calltimer(){
    console.log('calltimer==================');
    refresh();
    var int = setInterval("refresh()", 100000);

}

/*
$(document).ready(function ($) {

    console.log('refress==================');

    refresh();
    var int = setInterval("refresh()", 2000);

});
*/


function refresh() {

  $.ajax({
        url : '/ReadDataBase/',
        success: function(data) {
          console.log(data);

            if(data.all_pnr_db.length != 0){
                $('#recent_search').html(upload_pnr(data));

            }

        },
 })
};

$(document).on('click', '.collectionlist', function(e){
    var name = $(this).attr('name');

    e.preventDefault();
    $.ajax({
        type: 'POST',
        url : '/database_pnr/',
        data:{
            'database_Pnr':name,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){
            if (data.response_code == 200) {
                var win = window.open('', '_blank');

                if (win) {
                    //Browser has allowed it to be opened
                    win.focus();
                } else {
                    //Browser has blocked it
                    alert('Please allow popups for this website');
                }
                win.document.writeln(sentDataBasePnr(data));
                /*win.document.writeln('<html><head><title>test</title></head><body>dadasdasd</body></html>');*/
                win.document.close();
            }
            else {
                alert(data.response_code);
            }
        },

        failure: function() {
                alert('Got an error dude');
        },

    })

});




function upload_pnr(data){
  var httpresponce="";

    httpresponce += '<table id="RecentPnr" class="table table-striped " >';
    httpresponce += '    <thead >';
    httpresponce += '        <tr>';
    httpresponce += '            <th colspan="4" bgcolor="#00ffff">Recent PNR Search</th>';
    httpresponce += '        </tr>';

    httpresponce += '        <tr>';
    httpresponce += '            <th>PNR</th>';
    httpresponce += '            <th>Src-Dest</th>';
    httpresponce += '            <th>DOJ</th>';
    httpresponce += '        </tr>';
    httpresponce += '    </thead>';
    httpresponce += '    <tbody >';

  for(i=0; i < data.all_pnr_db.length; i++)
  {
    httpresponce += '        <tr>';
    httpresponce += '            <td>' + '<a href="#"  target="_blank" class="collectionlist" name="'+ data.all_pnr_db[i].RecentPnrNo +'" id="' + i + '">' + data.all_pnr_db[i].RecentPnrNo +'</a>' + '</td>';
    httpresponce += '            <td>' + data.all_pnr_db[i].Srcdest + '</td>';
    httpresponce += '            <td>' + data.all_pnr_db[i].DateOfJourney + '</td>';
    httpresponce += '        </tr>';

  }

    httpresponce += '    </tbody>';
    httpresponce += '</table>';

  return httpresponce;
}

function sentDataBasePnr(data){
    var httpresponce="";

    httpresponce += '<!DOCTYPE html>';
    httpresponce += '<html lang="en">';
    httpresponce += '    <head>';
    httpresponce += '        <title>PNR-' + data.pnr + '</title>';
    httpresponce += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />';

    httpresponce += '    </head>';
    httpresponce += '    <body>';
            httpresponce += '<div class="container-fluid">';
            httpresponce += '   <h4>PNR - ' +  data.pnr + '</h4>';
            httpresponce += '<table class="table ">';
            httpresponce += '    <td>';

            httpresponce += '       <table class="table table-bordered" >';
            httpresponce += '           <tbody>';
            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Train Name:</th>';
            httpresponce += '                 <td>' + data.train_name + '</td>';
            httpresponce += '               </tr>';
            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Train Number:</th>';
            httpresponce += '                 <td>' +  data.train_num + '</td>';
            httpresponce += '               </tr>';
            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">From Station:</th>';
            httpresponce += '                 <td>' + data.from_station.name + ' (' + data.from_station.code + ')' + '</td>';
            httpresponce += '               </tr>';

            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">To Station:</th>';
            httpresponce += '                 <td>' + data.to_station.name + ' (' + data.to_station.code + ')' + '</td>';
            httpresponce += '               </tr>';

            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Class:</th>';
            httpresponce += '                 <td>' + data.train_class + '</td>';
            httpresponce += '               </tr>';
            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Date Of Journey:</th>';
            httpresponce += '                 <td>' + data.doj + '</td>';
            httpresponce += '               </tr>';

            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Reserved Upto:</th>';
            httpresponce += '                 <td>' + data.reservation_upto.name + ' (' + data.reservation_upto.code + ')' + '</td>';
            httpresponce += '               </tr>';

            httpresponce += '               <tr>';
            httpresponce += '                 <th scope="row">Boarding Point:</th>';
            httpresponce += '                 <td>' + data.boarding_point.name + ' (' + data.boarding_point.code + ')' + '</td>';
            httpresponce += '               </tr>';
            httpresponce += '           </tbody>';
            httpresponce += '       </table>';

            httpresponce += '        </td>';
            httpresponce += '        <td>';

            httpresponce += '       <table class="table table-bordered">';
            httpresponce += '         <thead>';
            httpresponce += '           <tr>';
            httpresponce += '             <th>Sr.No</th>';
            httpresponce += '             <th>Booking Status</th>';
            httpresponce += '             <th>Current Status</th>';
            httpresponce += '           </tr>';
            httpresponce += '         </thead>';
            httpresponce += '         <tbody>';

                    $.each(data.passengers, function () {
            httpresponce += '           <tr>';
            httpresponce += '             <th scope="row">Pasenger ' +  this.no + '</th>';
            httpresponce += '             <td>' + this.booking_status + '</td>';
            httpresponce += '             <td>' + this.current_status + '</td>';
            httpresponce += '           </tr>';
                    });


            httpresponce += '           <tr>';
            httpresponce += '             <th scope="row">Charting Status</th>';
                          if (data.chart_prepared == 'N'){
            httpresponce += '               <td colspan="3">CHART NOT PREPARED</td>';
                          }
                          else{
            httpresponce += '               <td colspan="3">CHART PREPARED</td>';
                          }

            httpresponce += '           </tr>';
            httpresponce += '         </tbody>';
            httpresponce += '       </table>';
            httpresponce += '    </td>';
            httpresponce += '</table>';


            httpresponce += '</div>';

    httpresponce += '    </body>';
    httpresponce += '</html>';


    return httpresponce;
}







