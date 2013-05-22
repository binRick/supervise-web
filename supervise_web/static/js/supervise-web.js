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

function startSupervise(daemonId) {
    $.post('/daemon/' + daemonId + '/start_supervise');
}

function stopSupervise(daemonId) {
    $.post('/daemon/' + daemonId + '/stop_supervise');
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
    $(document).on('click', 'button.btn-start-supervise', function(event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        startSupervise(daemonId);
    });
    $(document).on('click', 'button.btn-stop-supervise', function(event) {
        var daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
        stopSupervise(daemonId);
    });
    $(document).on('mousedown', 'button', function() {
        stopRefreshing();
    });
    $(document).on('mouseup', 'button', function() {
        startRefreshing();
        refreshDaemonList(false);
    });
    startRefreshing(1000);
});