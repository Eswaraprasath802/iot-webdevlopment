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
                class: 'btn btn-success btn-generate-api-key',
                onClick: function(event) {
                var modal=$(event.data.modal);
                var device_name=modal.find('#api-name').val();
                var group_name=modal.find('#api-group').val();
                var description=modal.find('#api-remarks').val();
                if (device_name.length <3 || group_name.length <3){
                    animateCSS('.btn-generate-api-key', 'headShake');
                    return;
            }
            else{
                        $.post('/api/v1/generate/api/key',
                        {
                            'name':device_name,
                            'description':group_name,
                            'remarks':description
                        },
                        function(data, status, xhr){
                            if (status=='success'){
                            //    window.location.reload();
                              $(event.data.modal).modal('hide');
                              key=new Dialog('API Key Generated Successfully',data.key)
                              key.show();
                                $.get('/row/'+data.hash, function(random_data, status, xhr){
                                    if(status=="success"){
                                        $("#row_of_table").append(random_data);
                                        //TODO: Check if we need to reinitialize click event for delete button, since its dynamically added to DOM.
                                    }
                                });
                            }  
                            else{
                                alert('Error Occurred. Try Again');
                                 console.log("The status is Failed and there is some thing worng");
                            }
                        });
                    }
            }
        }
        ])
        d.show();
    });
});
$('.btn-to-add-api-key-group').on('click',function() {
    $.get('/api/dialog/api_key_groups', function(data, status, xhr) {
        d=new Dialog('Add Device Group',data
        );
        d.setButtons([
            {
                name: 'Create Group',
                class: 'btn btn-success btn-button-api',
                onClick: function(event) {
                    var modal =$(event.data.modal);
                    var group_name=modal.find('#group-name').val();
                    var description=modal.find('#api-remarks').val();
                    if (group_name.length <3 || description.length <5){
                        animateCSS('.btn-button-api', 'headShake');
                        return;
                    }
                    else{
                        $.post('/api/v1/get/api/group',
                        {
                            'name':group_name,
                            'description':description
                        },
                        function(data, status, xhr){
                            console.log(data);
                            if (status=='success'){
                            //    window.location.reload();
                              $(event.data.modal).modal('hide');
                            }
                            else{
                                alert('Error Occurred. Try Again');
                            }
                        });
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