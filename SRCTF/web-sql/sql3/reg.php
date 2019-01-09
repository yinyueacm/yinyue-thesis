<!doctype html>
<html>
<head>
    <title>Secdawg Login</title>
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
</head>
<body>
<nav class="navbar navbar-default" role="navigation">
    <div class="container-fluid">
        <div class="navbar-header">
            <img src="secdawgs.png" style="height: 80px"><span
                style="margin-left: 10px; font-size: 19px;line-height: 21px;height: 60px;">SecDawg Top Secret</span>
        </div>

    </div>
</nav>
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">The Old Register Page</h3>
                    <a href="index.php">Link to login index</a>
                </div>
                <div class="panel-body">
                    <form action="register.php" method="POST">
                        <div class="form-group">
                            <label for="reg_username">Username:</label>
                            <input type="text" id="reg_username" name="username" class="form-control">
                        </div>
                        <input type="submit" name="action" value="Register" class="btn btn-primary">
                    </form>
                </div>
            </div>

            <a href="register.txt">register.php source code</a>
        </div>
    </div>
</div>
</body>
</html>
