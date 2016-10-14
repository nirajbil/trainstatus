/**
 * Created by Niraj on 10/12/2016.
 */


$(document).on('submit','#trainArrival', function (e) {

    var source = $('#source').val();
    if(source.length == 0){
        alert('Please Enter Station Name');
        return false;
    }


    e.preventDefault();
    $.ajax({
        type: 'POST',
        url : '/train_Arrival/',
        data:{
            source:$('#source').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },

        success:function(data){

            console.log(data.response_code);
            if(data.response_code == 200)
            {
                $('#train_Arrival_Detail').html(trainArrivalAtStation(data));
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

    function trainArrivalAtStation(data){
        /*alert(data.response_code);*/
        var httpresponce="";
        httpresponce += '<table class="table table-bordered table-sm " id="myTable">';
        httpresponce += '<thead>';
        httpresponce += ' <tr>';
        httpresponce += '      <th>Train No</th>';
        httpresponce += '      <th>Train Name</th>';
        httpresponce += '      <th>scharr</th>';
        httpresponce += '      <th>schdep</th>';
        httpresponce += '      <th>delayarr</th>';
        httpresponce += '      <th>actarr</th>';
        httpresponce += '      <th>actdep</th>';
        httpresponce += '      <th>delaydep</th>';
        httpresponce += ' </tr>';
        httpresponce += '  </thead>';
        httpresponce += '  <tbody>';



        for(i=0;i<data.train.length;i++)
        {
            httpresponce += ' <tr>';
            console.log(data.train[i].number);
            httpresponce += '<td id="number-' + i + '">' + data.train[i].number + '</td>';

            console.log(data.train[i].name);
            httpresponce += '<td id="tname-' + i + '">' + data.train[i].name + '</td>';

            console.log(data.train[i].scharr);
            httpresponce += '<td id="scharr-' + i + '">' + data.train[i].scharr + '</td>';

            console.log(data.train[i].schdep);
            httpresponce += '<td id="schdep-' + i + '">' + data.train[i].schdep + '</td>';

            console.log(data.train[i].delayarr);
            httpresponce += '<td id="delayarr-' + i + '">' + data.train[i].delayarr + '</td>';

            console.log(data.train[i].actarr);
            httpresponce += '<td id="actarr-' + i + '">' + data.train[i].actarr + '</td>';

            console.log(data.train[i].actdep);
            httpresponce += '<td id="actdep-' + i + '">' + data.train[i].actdep + '</td>';

            console.log(data.train[i].delaydep);
            httpresponce += '<td id="delaydep-' + i + '">' + data.train[i].delaydep + '</td>';
            httpresponce += ' </tr>';
        }

        httpresponce += '</tbody></table>';

        return httpresponce;
    }
});





