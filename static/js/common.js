window.addEventListener('DOMContentLoaded', function() {
  [].forEach.call(document.querySelectorAll('.file-upload'), function(label) {
        var mark = label.querySelector('mark');
        label.querySelector('input').addEventListener('change', function() {
            mark.innerHTML  = this.value;
        });
    });
  });
