var container = document.getElementById('container');

function block(mClass, html) {
    return '<div class="' + mClass + '">' + html + '</div>';
}

for (var i = 0; i < 3; i++) {
    container.innerHTML += block('block', 'data');
}