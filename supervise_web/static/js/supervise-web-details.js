function onBackLinkClicked() {
    $('#daemon-single-view').fadeOut(100, function () {
        $('#daemon-overview').fadeIn(100);
        startRefreshing();
    });
}

function onAutostartCheckboxClicked(event) {
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

function onSaveButtonClicked() {
    var daemonId = $('#daemon-details').attr('data-daemon-id');
    var file_editor = $('#tab_content div:visible');
    var editor_tab = null;
    var data = {};
    if (file_editor.is($('#run_file'))) {
        editor_tab = $('#run_file_tab');
        data['filename'] = 'run';
        data['content'] = ace.edit('run_file').getSession().getValue();
    } else if (file_editor.is($('#run_user_file'))) {
        editor_tab = $('#run_user_file_tab');
        data['filename'] = 'run-user';
        data['content'] = ace.edit('run_user_file').getSession().getValue();
    }

    $.ajax({
        type: 'POST',
        url: '/daemon/' + daemonId + '/save_file',
        data: data,
        success: function () {
            editor_tab.removeData('modified');
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
                buttons: { 'Ok': function () {
                    $(this).dialog('close');
                } }
            });
        }
    });
}

function onRunFileTabClicked() {
    $('#tab_content').children().hide();
    $('#run_file').show();
    $('#file_tabs > div').removeClass('active');
    $('#run_file_tab').addClass('active');
    if ($('#run_file_tab').data('modified')) {
        $('#savebutton').show();
    } else {
        $('#savebutton').hide();
    }
}

function onRunUserFileTabClicked() {
    $('#tab_content').children().hide();
    $('#run_user_file').show();
    $('#file_tabs > div').removeClass('active');
    $('#run_user_file_tab').addClass('active');
    if ($('#run_user_file_tab').data('modified')) {
        $('#savebutton').show();
    } else {
        $('#savebutton').hide();
    }
}

function onLogFileTabClicked() {
    $('#tab_content').children().hide();
    $('#log_file').show();
    $('#file_tabs > div').removeClass('active');
    $('#log_file_tab').addClass('active');
    $('#savebutton').hide();
}

function onLogFile2TabClicked() {
    $('#tab_content').children().hide();
    $('#log_file2').show();
    $('#file_tabs > div').removeClass('active');
    $('#log_file2_tab').addClass('active');
    $('#savebutton').hide();
}

function onLogConfigButtonClicked() {
    var daemonId = $('#daemon-details').attr('data-daemon-id');
    var logLocations;
    $.ajax({
        url: '/daemon/' + daemonId + '/log_file_locations',
        async: false,
        success: function (data) {
            logLocations = data;
        }
    });
    var runLog = logLocations['run_log'] || '';
    var daemonLog = logLocations['daemon_log'] || '';

    var dialog = $('#dialog-widget');
    dialog.html(
        '<div id="edit_log_location_dialog">' +
            '<p><label for="run_log_file_location">run log file</label><input id="run_log_file_location" type="text" value="' + runLog + '"/></p>' +
            '<p><label for="daemon_log_file_location">run-user log file</label><input id="daemon_log_file_location" type="text" value="' + daemonLog + '" /></p>' +
            '</div>');
    dialog.dialog({
        title: 'Edit log file locations',
        resizable: false,
        width: 400,
        height: 180,
        modal: true,
        buttons: {
            'Save': function () {
                $.ajax({
                    url: '/daemon/' + daemonId + '/log_file_locations',
                    type: 'POST',
                    data: {
                        run_log: $('#run_log_file_location').val(),
                        daemon_log: $('#daemon_log_file_location').val()
                    },
                    async: false,
                    success: function () {
                        dialog.dialog('close');
                    }
                });
            },
            Cancel: function () {
                dialog.dialog('close');
            }
        }
    });
}

function onDetailsViewLoaded() {
    var names = ['run_file', 'run_user_file'];
    for (var i in names) {
        var editor = ace.edit(names[i]);
        editor.setTheme('ace/theme/monokai');
        editor.getSession().setMode('ace/mode/sh');
        editor.setShowPrintMargin(false);
        editor.getSession().on('change', function (event) {
            $('#file_tabs div.active').data('modified', true);
            $('#savebutton').show();
        });
        editor.commands.addCommand({
            name: 'save',
            bindKey: {win: 'Ctrl-S', mac: 'Command-S'},
            exec: onSaveButtonClicked,
            readOnly: true
        });
    }

    names = ['log_file', 'log_file2'];
    for (var i in names) {
        var editor = ace.edit(names[i]);
        editor.setTheme('ace/theme/monokai');
        editor.setShowPrintMargin(false);
    }

    $('#run_file').show();
    $('#run_file_tab').addClass('active');
    $('#daemon-overview').fadeOut(100, function () {
        $('#daemon-single-view').fadeIn(100);
    });
}

$(document).on('ready', function () {
    $(document).on('click', '#link-back', onBackLinkClicked);
    $(document).on('change', 'input#autostart', onAutostartCheckboxClicked);
    $(document).on('click', '#run_file_tab', onRunFileTabClicked);
    $(document).on('click', '#run_user_file_tab', onRunUserFileTabClicked);
    $(document).on('click', '#log_file_tab', onLogFileTabClicked);
    $(document).on('click', '#log_file2_tab', onLogFile2TabClicked);
    $(document).on('click', '#savebutton', onSaveButtonClicked);
    $(document).on('click', '#log_config', onLogConfigButtonClicked);
});