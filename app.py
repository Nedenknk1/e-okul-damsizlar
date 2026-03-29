<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Giriş Yap</title>
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div class="login-container">
    <h2>Giriş Yap</h2>
    <form method="post">
      <input type="text" name="username" placeholder="Kullanıcı Adı" required>
      <input type="password" name="password" placeholder="Şifre" required>
      <input type="submit" value="Giriş">
    </form>
  </div>
</body>
</html>
