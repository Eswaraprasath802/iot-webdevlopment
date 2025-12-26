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

$('.btn-api-switch').on('change',function(){
    var api_keys=$(this).attr('id');
    var status=$(this).is(":checked"); 
    var badge=$(this).parent().parent().parent().find('.api-status-badge');
    $.post('/enable/button',{
        'id':api_keys,
        'status':status
        
    },
    function(data, status, xhr){
        if (data.key){
            $(badge).removeClass('.hai').addClass('.welcome').html('Online');
        }
        else{
            $(badge).removeClass('.welcome').addClass('.hai').html('Offline');
        }
    }
    
);
});
$('.btn-to-add-device').on('click',function(){
    $.get('/add/device',function(data,status,xhr){
        j=new Dialog("Add devices",data);
        j.setButtons([
            {
                name:"Register",
                class:"btn bg-gradient-warning btn-register-devices ",
                onClick:function(event){
                    var modal=$(event.data.modal);
                    var name=modal.find('#device-name').val();
                    var dtype=modal.find('#device-type').val();
                    var group=modal.find('#api-key').val();
                    var remarks=modal.find('#device-remarks').val();
                    $.post("device/add/device_api",{
                        "name":name,
                        "type":dtype,
                        "group":group,
                        "remarks":remarks   
                    },
                    function(data,status,xhr){
                        if (status=="success"){
                            n=new Toast ("Device Registered","now","Device has been registed sucessfully");
                            n.show();
                        }
                        $(event.data.modal).modal('hide');
                }).fail(function(xhr,status,error){
                    n=new Toast ("error","now","SomeThing went wrong");
                            n.show();

                })
                
            }
            
        }
    ])
    j.show()
})
})
$('.btn-to-add-api-key').on('click',function() {
    $.get('/api/dialog/api_keys', function(data, status, xhr) {
        d=new Dialog('Add API',data);
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
                                            APIkeyListerners()
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
            d=new Dialog('Add API Group',data
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
        
        $('.delete-button').on('click',function(){
            var api_key=$(this).attr('id');
            var orginal_key=$(this).attr('importantid')
            // $.get('/row/'+data.hash, function(random_data, status, xhr){
            
            $.get('api/dialog/api_key_delete/'+api_key,function(variable_data,status,xhr){
                h=new Dialog('Delete API Group',variable_data);
                h.setButtons([
                    {
                        name:"Delete button",
                        class:'btn bg-gradient-success btn-delete',
                        onClick:function(event){
                            $.get('api/delete/database/'+orginal_key,function(singular_data,status,xhr){
                                if (status=='success'){
                                    console.log("delte databse sucessfull")
                                    var modal =$(event.data.modal);
                                    $(modal).modal('hide');
                                    $("#row" + orginal_key).remove();
                                    
                                }
                                
                            })
                        }
                    }
                ])
                h.show();
            })
            
        })
        
        function APIkeyListerners(){
            $('.btn-api-switch').on('change',function(){
                var api_keys=$(this).attr('id');
                var status=$(this).is(":checked"); 
                var badge=$(this).parent().parent().parent().find('.api-status-badge');
                $.post('/enable/button',{
                    'id':api_keys,
                    'status':status
                    
                },
                function(data, status, xhr){
                    if (data.key){
                        $(badge).removeClass('.hai').addClass('.welcome').html('Online');
                    }
                    else{
                        $(badge).removeClass('.welcome').addClass('.hai').html('Offline');
                    }
                }
                
            );
        });
        
        
        $('.delete-button').on('click',function(){
            var api_key=$(this).attr('id');
            var orginal_key=$(this).attr('importantid')
            // $.get('/row/'+data.hash, function(random_data, status, xhr){
            
            $.get('api/dialog/api_key_delete/'+api_key,function(variable_data,status,xhr){
                h=new Dialog('Delete API Group',variable_data);
                h.setButtons([
                    {
                        name:"Delete button",
                        class:'btn bg-gradient-success btn-delete',
                        onClick:function(event){
                            $.get('api/delete/database/'+orginal_key,function(singular_data,status,xhr){
                                if (status=='success'){
                                    console.log("delte databse sucessfull")
                                    var modal =$(event.data.modal);
                                    $(modal).modal('hide');
                                    $("#row" + orginal_key).remove();
                                    
                                }
                                
                            })
                        }
                    }
                ])
                h.show();
            })
            
        })
        
        
        
    }