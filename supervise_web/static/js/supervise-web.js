function refreshDaemonList(synchronous) {
    $.ajax({
        url: '/_daemons.html',
        async: synchronous != true,
        cache: false,
        success: function(data) {
            $('#daemon-overview').html(data);
        }
    });
}

function startRefreshing(interval) {
    if (interval === undefined) {
        interval = 'defaultInterval' in startRefreshing ? startRefreshing.defaultInterval : 1;
    } else {
        startRefreshing.defaultInterval = interval;
    }

    if ('intervalId' in startRefreshing) stopRefreshing();
    startRefreshing.intervalId = window.setInterval(refreshDaemonList, interval);
}

function stopRefreshing() {
    if ('intervalId' in startRefreshing) {
        clearInterval(startRefreshing.intervalId);
        delete startRefreshing.intervalId;
    }
}

function startDaemon(daemonId) {
    $.post('/daemon/' + daemonId + '/start');
}

function stopDaemon(daemonId) {
    $.post('/daemon/' + daemonId + '/stop');
}

$(document).on('ready', function() {
    refreshDaemonList(true);
    $(document).on('click', 'button.btn-start', function(event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        startDaemon(daemonId);
    });
    $(document).on('click', 'button.btn-stop', function(event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        stopDaemon(daemonId);
    });
    $(document).on('mousedown', 'button', function() {
        stopRefreshing();
    });
    $(document).on('mouseup', 'button', function() {
        startRefreshing();
    });
    startRefreshing(1000);
});