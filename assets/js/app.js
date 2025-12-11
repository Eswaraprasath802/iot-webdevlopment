d = new Dialog("Hello World", "Quote not loaded, click Show Quote button to motivate you.", {
    "backdrop": "static"
});
d.setButtons([
    {
        name: "Show Quote",
        class: "btn-primary",
        onClick: function(event){
            console.log(event);
            var settings = {
                "url": "https://type.fit/api/quotes",
                "method": "GET",
                "timeout": 0,
              };
              
            $.ajax(settings).done(function (response) {
                console.log(response);
                var items = JSON.parse(response);
                var quote = items[Math.floor(Math.random()*items.length)];
                var template = `<figure>
                    <blockquote class="blockquote text-center">
                    <p class="ps-2">${quote.text}</p>
                    </blockquote>
                    <figcaption class="blockquote-footer text-center">
                    <cite title="Source Title">${quote.author}</cite>
                    </figcaption>
                </figure>`;
                $(event.data.modal).find(".modal-body").html(template);
            });
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
]);
d.show();
