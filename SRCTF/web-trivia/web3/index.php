<!doctype html>
<html>
<script>
    function hash(str, seed) {
        /*jshint bitwise:false */
        var i, l,
            hval = (seed === undefined) ? 0x811c9dc5 : seed;

        for (i = 0, l = str.length; i < l; i++) {
            hval ^= str.charCodeAt(i);
            hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
        }
        return hval >>> 0;
    }


    function checkpassword(){
        var x = document.forms["loginform"]["password"].value;
        if (hash(x)==885536277){
            return true;
        }
        alert("Sorry, wrong password.");
        return false;
    }
</script>
<head>
    <title>Secdawg TopSecret Login</title>
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
</head>
<body>
<nav class="navbar navbar-default" role="navigation">
    <div class="container-fluid">
        <div class="navbar-header">
            <img src="secdawgs.png" style="height: 80px"><span style="margin-left: 10px; font-size: 19px;line-height: 21px;height: 60px;">Secdawg</span>
        </div>

    </div>
</nav>
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <div class="panel panel-primary" style="margin-top:50px">
                <div class="panel-heading">
                    <h3 class="panel-title">Welcome to secdawg's safe</h3>
                </div>
                <div class="panel-body">
                    <form name="loginform" action="login.php" method="POST" onsubmit="return checkpassword();">
                        <fieldset>
                            <div class="form-group">
                                <label for="username">Username:</label>
                                <input type="text" id="username" name="username" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="password">Password:</label>
                                <div class="controls">
                                    <input type="password" id="password" name="password" class="form-control">
                                </div>
                            </div>
                            <div class="form-actions">
                                <input type="submit" value="Get the secret!" class="btn btn-primary">
                            </div>
                        </fieldset>
                    </form>
                </div>
            </div>
            <div>For questions, please contact "admin"</div>
        </div>
    </div>
</div>
</body>
</html>
