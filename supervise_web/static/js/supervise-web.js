function refreshDaemonList(synchronous) {
    $.ajax({
        url: '/_daemons.html',
        async: synchronous != true,
        cache: false,
        success: function (data) {
            $('#error-panel').text('');
            $('#daemons-list').html(data);
            $('#refresh-spinner img').effect('shake', {distance: 5, times: 1});
        },
        error: function (data) {
            $('#error-panel').text('Unable to retrieve data from server!');
        }
    });
}

function startRefreshing() {
    var interval = $('#refresh-slider').slider('value');
    var sliderLabel = $('#refresh-control label');
    if (interval == 0) {
        sliderLabel.text('no page refresh');
    } else if (interval == 1) {
        sliderLabel.text('refreshing every second');
    } else {
        sliderLabel.text('refreshing every ' + interval + ' seconds');
    }

    if ('intervalId' in startRefreshing) {
        stopRefreshing();
        if (interval == 0) return;
    }
    startRefreshing.intervalId = window.setInterval(refreshDaemonList, interval * 1000);
    $('#refresh-spinner').css('visibility', 'visible');
}

function stopRefreshing() {
    if ('intervalId' in startRefreshing) {
        clearInterval(startRefreshing.intervalId);
        delete startRefreshing.intervalId;
    }
    $('#refresh-spinner').css('visibility', 'hidden');
}

function startDaemon(daemonId) {
    $.post('/daemon/' + daemonId + '/start');
}

function stopDaemon(daemonId) {
    $('#dialog-widget').html('You are about to stop this daemon. Are you sure you want to do this?');
    $('#dialog-widget').dialog({
        title: 'Confirm',
        resizable: false,
        width: 300,
        height: 150,
        modal: true,
        buttons: {
            'Stop Daemon': function () {
                $(this).dialog('close');
                $.post('/daemon/' + daemonId + '/stop');
            },
            Cancel: function () {
                $(this).dialog('close');
            }
        }
    });
}

function startSupervise(daemonId) {
    $.post('/daemon/' + daemonId + '/start_supervise');
}

function stopSupervise(daemonId) {
    $.post('/daemon/' + daemonId + '/stop_supervise');
}

$(document).on('ready', function () {
    refreshDaemonList(true);

    $(document).on('click', 'button.btn-start', function (event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        startDaemon(daemonId);
    });

    $(document).on('click', 'button.btn-stop', function (event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        stopDaemon(daemonId);
    });

    $(document).on('click', 'button.btn-start-supervise', function (event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        startSupervise(daemonId);
    });

    $(document).on('click', 'button.btn-stop-supervise', function (event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        stopSupervise(daemonId);
    });

    $(document).on('mousedown', 'button', function () {
        stopRefreshing();
    });

    $(document).on('mouseup', 'button', function () {
        startRefreshing();
        refreshDaemonList(false);
    });

    $("#refresh-slider").slider({
        min: 0,
        max: 5,
        value: 1,
        change: startRefreshing
    });

    $(document).on('click', 'div[data-daemon-id]', function (event) {
        if ($(event.target).is('button')) return;
        stopRefreshing();
        $('div#daemon-overview').fadeOut(100, function () {
            $('div#daemon-single-view').fadeIn(100);
        });
    });

    startRefreshing();
});