
var objects = 
 {
    todos: new Backbone.Collection([
        {
            name: "a1"
        },
        {
            name: "b1"
        }
    ])
};

var el = document.getElementById("thingView");
var model = new Backbone.Model(objects);
rivets.bind(el, { model: model });
    setInterval(function () {
        objects.todos.at(-1).set({ name: objects.todos.at(-1).get("name")+"'s gone" });
        objects.todos.push(
            {
                name: "woo"
            });
    
    }, 1000)