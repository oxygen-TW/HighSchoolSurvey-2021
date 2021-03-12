
function Q2check(val) {
    document.getElementById("Q2").disabled = !val;

    if (val == 0) {
        document.getElementById("Q2").value = "";
    }
}

function Q5check(val) {
    var Q6node = document.getElementsByName("Q6");
    Q6node.forEach(element => element.disabled = !val);

    if (val == 0) {
        Q6node.forEach(element => element.checked = false);
    }
}

function check() {
    if (document.getElementsByName("stuId")[0].value == "") {
        alert("學號未填寫");
        return;
    }
    var r = document.getElementsByName("sex");
    if (r[0].checked == false && r[1].checked == false) {
        alert("性別未選擇");
        return;
    }

    var r = document.getElementsByName("grade");
    if (r[0].checked == false && r[1].checked == false && r[2].checked == false) {
        alert("年級未選擇");
        return;
    }

    if (document.getElementsByName("dept")[0].value == "") {
        alert("科別未填寫");
        return;
    }

    var r = document.getElementsByName("Q1");
    if (r[0].checked == false && r[1].checked == false) {
        alert("第一題未選擇");
        return;
    } else {
        //如果第一題選是
        if (r[0].checked == true) {
            //檢查第二題
            var r = document.getElementsByName("Q2");
            if (r[0].value == "") {
                alert("第二題未填寫");
                return;
            }
        }
    }

    var r = document.getElementsByName("Q3");
    if (r[0].checked == false && r[1].checked == false) {
        alert("第三題未選擇");
        return;
    }

    var r = document.getElementsByName("Q4");
    if (r[0].checked == false && r[1].checked == false) {
        alert("第四題未選擇");
        return;
    }

    var r = document.getElementsByName("Q5");
    if (r[0].checked == false && r[1].checked == false) {
        alert("第五題未選擇");
        return;
    } else {
        //如果第五題選是
        if (r[0].checked == true) {
            //檢查第六題
            var r = document.getElementsByName("Q6");
            if (r[0].checked == false && r[1].checked == false) {
                alert("第六題未選擇");
                return;
            }
        }
    }
    var r = document.getElementsByName("Q7");
    if (r[0].checked == false && r[1].checked == false) {
        alert("第七題未選擇");
        return;
    }
    //set schoolcode
    document.getElementById("schoolCodeCtrl").value = getSchoolCode();
    document.getElementById("mainForm").submit();
}

//Source: https://ithelp.ithome.com.tw/articles/10190254
function getSchoolCode() {
    var url = location.href;

    //再來用去尋找網址列中是否有資料傳遞(QueryString)
    if (url.indexOf('?') != -1) {
        //之後去分割字串把分割後的字串放進陣列中
        var ary1 = url.split('?');
        var ary2 = ary1[1].split('&');
        var ary3 = ary2[0].split('=');

        var schoolId = ary3[1];
        return schoolId;
    }
}