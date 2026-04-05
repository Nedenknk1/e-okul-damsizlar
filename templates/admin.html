<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Admin Paneli</title>

  <style>
    body{
      font-family: Arial;
      background:#f4f6f8;
      margin:0;
    }

    header{
      background:#222;
      color:white;
      padding:15px;
      text-align:center;
    }

    .container{
      width:95%;
      margin:auto;
      margin-top:20px;
    }

    .tabs{
      display:flex;
      gap:10px;
      margin-bottom:10px;
    }

    .tab{
      padding:10px 20px;
      background:#ddd;
      cursor:pointer;
      border-radius:6px;
    }

    .tab.active{
      background:#4a90e2;
      color:white;
    }

    .tab-content{
      display:none;
      background:white;
      padding:15px;
      border-radius:10px;
      box-shadow:0 0 10px rgba(0,0,0,0.1);
    }

    .tab-content.active{
      display:block;
    }

    table{
      width:100%;
      border-collapse:collapse;
    }

    th,td{
      border:1px solid #ddd;
      padding:8px;
      text-align:center;
    }

    input{
      width:60px;
      text-align:center;
    }

    .logout{
      float:right;
      color:white;
      text-decoration:none;
      margin-right:20px;
    }
  </style>
</head>

<body>

<header>
  <a class="logout" href="{{ url_for('logout') }}">Çıkış Yap</a>
  <h2>Admin Paneli</h2>
</header>

<div class="container">

<div class="tabs">
  <div class="tab active" onclick="showTab('d1')">1. Dönem</div>
  <div class="tab" onclick="showTab('d2')">2. Dönem</div>
</div>

<!-- 1. DÖNEM -->
<div id="d1" class="tab-content active">
<form method="post">
<input type="hidden" name="form_type" value="1">

<table>
<tr>
<th>Öğrenci</th>
<th>1.Yazılı</th>
<th>2.Yazılı</th>
<th>1.Perf</th>
<th>2.Perf</th>
<th>Ortalama</th>
</tr>

{% for u, info in users.items() %}
{% if info.role == "student" %}
<tr>
<td>{{ u }}</td>

{% for k in ["yazili1","yazili2","perf1","perf2"] %}
<td>
<input name="grades_1_{{u}}_{{k}}" value="{{ info.grades['1_donem'][k] if info.grades['1_donem'][k] is not none else '' }}">
</td>
{% endfor %}

<td>
{% set v = info.grades['1_donem'].values() | select('number') | list %}
{{ (v|sum / v|length)|round(2) if v else '' }}
</td>

</tr>
{% endif %}
{% endfor %}
</table>

<br>
<button type="submit">Kaydet</button>
</form>
</div>

<!-- 2. DÖNEM -->
<div id="d2" class="tab-content">
<form method="post">
<input type="hidden" name="form_type" value="2">

<table>
<tr>
<th>Öğrenci</th>
<th>1.Yazılı</th>
<th>2.Yazılı</th>
<th>1.Perf</th>
<th>2.Perf</th>
<th>Proje</th>
<th>2.Dönem Ort</th>
<th>Yıl Sonu</th>
</tr>

{% for u, info in users.items() %}
{% if info.role == "student" %}
<tr>
<td>{{ u }}</td>

{% for k in ["yazili1","yazili2","perf1","perf2","proje"] %}
<td>
<input name="grades_2_{{u}}_{{k}}" value="{{ info.grades['2_donem'][k] if info.grades['2_donem'][k] is not none else '' }}">
</td>
{% endfor %}

<!-- 2 dönem ort -->
<td>
{% set v2 = info.grades['2_donem'].values() | select('number') | list %}
{{ (v2|sum / v2|length)|round(2) if v2 else '' }}
</td>

<!-- yıl sonu -->
<td>
{% set v1 = info.grades['1_donem'].values() | select('number') | list %}
{% set v2 = info.grades['2_donem'].values() | select('number') | list %}

{% set a1 = (v1|sum / v1|length) if v1 else 0 %}
{% set a2 = (v2|sum / v2|length) if v2 else 0 %}

{{ ((a1 + a2) / 2) | round(2) }}
</td>

</tr>
{% endif %}
{% endfor %}
</table>

<br>
<button type="submit">Kaydet</button>
</form>
</div>

</div>

<script>
function showTab(id){
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

  document.querySelector(`[onclick="showTab('${id}')"]`).classList.add('active');
  document.getElementById(id).classList.add('active');
}
</script>

</body>
</html>