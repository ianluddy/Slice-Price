/* Globals */
var stats = {};
var page_main = undefined;
var page_title =  undefined;
var spinner = undefined;
var pizza_info = {};
var vendor_info = {};

$(document).ready(function () {
    create_components();
    load_counts();
    load_vendors();

    // Cache
    page_main = $("#page_main");
    page_title = $("#page_title");
    spinner = $("#spinner");

    $.when(
        ajax_load('templates.html', {}, attach_templates)
    ).done(templates_loaded);
});

function create_components(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
}

function compile_templates(){
    pizza_title_tmpl = Handlebars.compile($("#pizza_title_tmpl").html());
    pizza_tmpl = Handlebars.compile($("#pizza_tmpl").html());
}

function attach_templates(input){
    $("#tmpl_holder").html(input);
}

function templates_loaded(){
    attach_templates();
    compile_templates();
    add_handlers();
}

function add_handlers(){
    $("#side-menu li.tab").on("click", function(){
        $(this).addClass("active").siblings().removeClass("active");
        window[$(this).attr("target")]();
    });
    $("#side-menu li.tab").first().click();
}

function load_counts(){
    ajax_load("stats", {}, update_counts);
}

function load_vendors(){
    ajax_load("vendors", {}, function(input){vendor_info=input;});
}

function update_counts(input){
    stats = input;
    $("#pizza_cnt").text(input["pizza"]);
    $("#side_cnt").text(input["sides"]);
    $("#dessert_cnt").text(input["desserts"]);
    $("#drink_cnt").text(input["drinks"]);
    $("#combo_cnt").text(input["combos"]);
}

function load_pizza(){
    $.when(
        ajax_load("pizza", {}),
        ajax_load("pizza/bases", {}, function(input){pizza_info["bases"] = input;}),
        ajax_load("pizza/toppings", {}, function(input){pizza_info["toppings"] = input;}),
        ajax_load("pizza/styles", {}, function(input){pizza_info["styles"] = input;}),
        ajax_load("pizza/sizes", {}, function(input){pizza_info["sizes"] = input;}),
        ajax_load("pizza/diameters", {}, function(input){pizza_info["diameters"] = input;}),
        ajax_load("pizza/slices", {}, function(input){pizza_info["slices"] = input;})
    ).done(draw_pizza);
}

function pizza_filters(){
    return {}
}

function draw_pizza(input){
    //clear();

    //$(page_title).html(pizza_title_tmpl({"title": "Pizza"}));
    pizza_info["vendors"] = vendor_info;
    $(page_main).html(pizza_tmpl(pizza_info));
}

function clear(){
    $(page_title).empty();
    $(page_main).empty();
}

function load_sides(){
    console.log("sides");
}

function toaster(){
    setTimeout(function() {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            showMethod: 'slideDown',
            timeOut: 4000
        };
        toastr.success('Responsive Admin Theme', 'Welcome to INSPINIA');
    }, 1300);
}


function ajax_load(func, args, callback){
    show_loader();
    return $.ajax({
        url: func,
        data: args
    }).done(function(input){
        hide_loader();
        if (callback)
            callback(input);
    });
}

function show_loader(){
    $(page_main).animate({"opacity": 0.4}, 200);
    $(spinner).fadeIn(200);
}

function hide_loader(){
    $(page_main).animate({"opacity": 1}, 200);
    $(spinner).fadeOut(200);
}
