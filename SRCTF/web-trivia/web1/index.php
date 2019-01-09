<!doctype html>
<html>
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
                    <form action="login.php" method="POST">
                        <fieldset>
                            <div class="form-group">
                                <label for="username">Username:</label>
                                <input type="text" id="username" name="username" class="form-control">
                            </div>
                            <div class="form-group">
                                <!--Reminder: your password is qwerty654321-->
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
