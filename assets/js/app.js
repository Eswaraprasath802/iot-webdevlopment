const animateCSS = (element, animation, prefix = 'animate__') =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = document.querySelector(element);

    node.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
      event.stopPropagation();
      node.classList.remove(`${prefix}animated`, animationName);
      resolve('Animation ended');
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
  });


$('.btn-to-add-api-key').on('click',function() {
    $.get('/api/dialog/api_keys', function(data, status, xhr) {
        d=new Dialog('Add Device',data);
        d.setButtons([
            {
                name: 'Generate Key',
                class: 'btn btn-success',
                onClick: function(event) {
                     $(event.data.modal).modal('hide');
            }
        }
        ])
        d.show();
    });
});
$('.btn-to-add-api-key-group').on('click',function() {
    $.get('/api/dialog/api_key_groups', function(data, status, xhr) {
        d=new Dialog('Add Device Group',data
            ,{"backdrop": "static"}
        );

        d.setButtons([
            {
                name: 'Generate Key',
                class: 'btn btn-success btn-button-api',
                onClick: function(event) {
                    var modal =$(event.data.modal);
                    var group_name=modal.find('#group-name').val();
                    console.log(group_name);
                    backdrop = true;
                    if (group_name.length == 0) {
                        animateCSS('.btn-button-api', 'headShake');
                        return;
                    }

            }
        },
         {
        name: "Close",
        class: "btn-warning",
        // dismiss: true,
        onClick: function(event){
            $(event.data.modal).modal('hide');
        }
    }
        ])
        d.show();
    });
});