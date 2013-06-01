function refreshDaemonList(synchronous) {
    $.ajax({
        url: '/_daemons',
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

    if ('intervalId' in startRefreshing) stopRefreshing();
    if (interval == 0) return;
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

function onDaemonRowClicked (event) {
    if ($(event.target).is('button')) return;
    stopRefreshing();
    var daemonId = $(event.target).attr('data-daemon-id');
    if (daemonId === undefined)
        daemonId = $(event.target).parents('div[data-daemon-id]').attr('data-daemon-id');
    $('#daemon-single-view').load('/daemon/' + daemonId + '/_details', function() {
        $('#daemon-overview').fadeOut(100, function () {
            $('#daemon-single-view').fadeIn(100);
        });
    });
}

function onBackLinkClicked (event) {
    $('#daemon-single-view').fadeOut(100, function () {
        $('#daemon-overview').fadeIn(100);
        startRefreshing();
    });
}

function onAutostartCheckboxClicked (event) {
    var checkbox = $(event.target);
    var daemonId = $('#daemon-details').attr('data-daemon-id');
    var url = '/daemon/' + daemonId + '/';
    url += checkbox.is(':checked') ? 'autostart' : 'no_autostart';
    checkbox.hide();
    $('.autostart img').show();
    $.post(url, function () {
        checkbox.show();
        $('.autostart img').hide();
    });
}

function onRunFileTabClicked (targetTextarea) {
    $('#tab_content').children().hide();
    targetTextarea.show();
    if (targetTextarea.data('modified')) {
        $('#savebutton').show();
    } else {
        $('#savebutton').hide();
    }
}

function onLogFileTabClicked (targetTextarea) {
    $('#tab_content').children().hide();
    $('#savebutton').hide();
    targetTextarea.show();
}

function onSaveButtonClicked () {
    var daemonId = $('#daemon-details').attr('data-daemon-id');
    var textarea = $('#tab_content textarea:visible');
    var data = {'content': textarea.val()};
    if (textarea.is($('#run_file'))) {
        data['filename'] = 'run';
    } else if (textarea.is($('#run_user_file'))) {
        data['filename'] = 'run-user';
    }

    $.ajax({
        type: 'POST',
        url: '/daemon/' + daemonId + '/save_file',
        data: data,
        success: function () {
            textarea.removeData('modified');
            $('#savebutton').hide();
        },
        error: function (jqXHR) {
            console.log(jqXHR);
            $('#dialog-widget').html('Could not save file - ' + jqXHR.statusText);
            $('#dialog-widget').dialog({
                title: 'Something went wrong',
                resizable: false,
                width: 310,
                height: 120,
                modal: true,
                buttons: { 'Ok': function () { $(this).dialog('close'); } }
            });
        }
    });
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

    $('#refresh-slider').slider({
        min: 0,
        max: 5,
        value: 3,
        change: startRefreshing
    });

    $(document).on('click', '#daemons-list div[data-daemon-id]', onDaemonRowClicked);
    $(document).on('click', '.link-back', onBackLinkClicked);
    $(document).on('change', 'input#autostart', onAutostartCheckboxClicked);

    $(document).on('click', '#run_file_tab', function () {
        onRunFileTabClicked($('#run_file'));
    });
    $(document).on('click', '#run_user_file_tab', function () {
        onRunFileTabClicked($('#run_user_file'));
    });
    $(document).on('click', '#log_file_tab', function () {
        onLogFileTabClicked($('#log_file'));
    });
    $(document).on('click', '#log_file2_tab', function () {
        onLogFileTabClicked($('#log_file2'));
    });

    $(document).keydown(function(event) {
        if (String.fromCharCode(event.which).toLowerCase() == 's' && event.ctrlKey || event.which == 19) {
            event.preventDefault();
            onSaveButtonClicked();
        }
    });

    $(document).on('keypress', '#tab_content textarea', function (event) {
        $(event.target).data('modified', true);
        $('#savebutton').show();
        console.log(event.ctrlKey + ' ' + event.keyCode + ' ' + 's'.charCodeAt(0));
    });

    $(document).on('click', '#savebutton', onSaveButtonClicked);

    startRefreshing();
});