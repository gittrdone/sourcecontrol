function getData(repoNum) {
    $.getJSON("/status/" + repoNum, function (data) {
        var repo;
        console.log(data);
        if (data.status == 3) {
            // Data is ready!
            $("#status-" + repoNum).remove();
            repo = $("#repo-" + repoNum);

            $(
'<div class="large-1 columns" style="font-size:22px;color:darkblue;margin-top: 20px;">\
{0}\
<br/><div style="font-size:15px;color:black;">files</div>\
</div>\
<div class="large-1 columns" style="font-size:22px;color:darkblue;margin-top: 20px;">\
{1}\
<br/><div style="font-size:15px;color:black;">commits</div>\
</div>'
                .replace("{0}", data.numFiles)
                .replace("{1}", data.numCommits))
                .insertAfter(repo);

            var url = "repo/detail/" + repoNum;
            $("#name-" + repoNum).wrap('<a href="' + url + '"></a>');
        }
    });
}

function updateProgress() {
    var workingRepos = document.querySelectorAll('[id^="status-"]');

    var i, repo, repoNum;
    for (i = 0; i < workingRepos.length; ++i) {
        repo = workingRepos[i];
        repoNum = repo.id.slice(7);

        getData(repoNum);
    }
}

// Call every 5 seconds
setInterval(updateProgress, 5000);