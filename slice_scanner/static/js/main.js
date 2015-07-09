/* Globals */
var stats = {};
var spinner, page_title, page_main;
var pizza_info = {};
var vendor_list = [];
var vendor_info = {};
var title_tmpl, filter_group_tmpl, pizza_table_head_tmpl, pizza_table_row_tmpl, table_tmpl, table_page_tmpl;

$(document).ready(function () {
    load_counts();
    load_vendors();
    cache_elements();

    $.when(
        ajax_load('templates.html', {}, attach_templates)
    ).done(templates_loaded);
});

function templates_loaded(){
    attach_templates();
    compile_templates();
    add_tab_handlers();
}

function init_checkboxes(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
}

function init_footable(){
    $('.footable').footable();
}

function cache_elements(){
    page_main = $("#page_main");
    page_title = $("#page_title");
    spinner = $("#spinner");
}

function compile_templates(){
    title_tmpl = Handlebars.compile($("#title_tmpl").html());
    filter_group_tmpl = Handlebars.compile($("#filter_group_tmpl").html());
    pizza_table_head_tmpl = Handlebars.compile($("#pizza_table_head_tmpl").html());
    pizza_table_row_tmpl = Handlebars.compile($("#pizza_table_row_tmpl").html());
    table_tmpl = Handlebars.compile($("#table_tmpl").html());
    table_page_tmpl = Handlebars.compile($("#table_page_tmpl").html());
}

function attach_templates(input){
    $("#tmpl_holder").html(input);
}

function add_tab_handlers(){
    $("#side-menu li.tab").on("click", function(){
        $(this).addClass("active").siblings().removeClass("active");
        window[$(this).attr("target")]();
    });
    $("#side-menu li.tab").first().click();
}

function add_body_handlers(){
    $(".sl-btn").on("mouseout", function(){$(this).removeClass("focus").blur();});
}

function load_counts(){
    ajax_load("stats", {}, update_counts);
}

function load_vendors(){
    ajax_load("vendors", {}, function(input){
        vendor_info=input;
        for( var vendor_id in input){
            vendor_list.push(input[vendor_id].name)
        }
    });
}

function update_counts(input){
    stats = input;
    $("#pizza_cnt").text(input["pizza"]);
    $("#side_cnt").text(input["sides"]);
    $("#dessert_cnt").text(input["desserts"]);
    $("#drink_cnt").text(input["drinks"]);
    $("#combo_cnt").text(input["combos"]);
}

function load_pizza_page(){
    show_loader();
    $.when(
        //ajax_load("pizza", {}, function(input){pizza_info["pizza"] = input;}),
        ajax_load("pizza/bases", {}, function(input){pizza_info["bases"] = input;}),
        ajax_load("pizza/toppings", {}, function(input){pizza_info["toppings"] = input;}),
        ajax_load("pizza/styles", {}, function(input){pizza_info["styles"] = input;}),
        ajax_load("pizza/sizes", {}, function(input){pizza_info["sizes"] = input;}),
        ajax_load("pizza/diameters", {}, function(input){pizza_info["diameters"] = input;}),
        ajax_load("pizza/slices", {}, function(input){pizza_info["slices"] = input;})
    ).done(draw_page_pizza);
}

//function reload_pizza(){
//    $.when(
//        ajax_load("pizza", {}, function(input){pizza_info["pizza"] = input;})
//    ).done(draw_page_pizza);
//}

function draw_table_template(){
    $(page_main).html(table_page_tmpl());
}

function refresh_pizza(){

}

function get_pizza_filters(){
    return {}
}

function add_filter(dom, id, items, theme, style, active){
    $(dom).append(filter_group_tmpl({
        "id": id,
        "title": id.toUpperCase(),
        "items": items,
        "theme": theme,
        "style": style,
        "active": active
    }));
}

function get_filter(id){
    var filtered = [];
    $("#" + id + " .sl-btn.active").each(function(){filtered.push($(this).text())});
    if (filtered.length > 0)
        return filtered;
    return undefined;
}

function get_num_filter(id){
    var filtered = [];
    $("#" + id + " .sl-btn.active").each(function(){filtered.push(parseFloat($(this).text()))});
    if (filtered.length > 0)
        return filtered;
    return undefined;
}

function add_table(title, page_size, head_tmpl, body_tmpl, data){
    $("#sl-table-wrapper").append(table_tmpl({
        "title": title,
        "page_size": page_size,
        "head": head_tmpl(),
        "body": body_tmpl({"data": data})
    }));
    init_footable();
}

function draw_page_pizza(){
    draw_table_template();

    // Add filters
    var filter_wrapper = $("#sl-filter-wrapper");
    add_filter(filter_wrapper, "vendors", vendor_list, "danger", "btn-outline", "active");
    add_filter(filter_wrapper, "crusts", pizza_info["bases"], "warning", "btn-outline", "active");
    add_filter(filter_wrapper, "toppings", pizza_info["toppings"], "primary", "btn-outline", "");
    add_filter(filter_wrapper, "sizes", pizza_info["diameters"], "info", "btn-circle btn-outline", "active");
    add_filter(filter_wrapper, "slices", pizza_info["slices"], "info", "btn-circle btn-outline", "active");
    init_checkboxes();

    // Add table
    add_pizza_table();

    add_body_handlers();
    hide_loader();
}

function add_pizza_table(){
    console.log(get_filters())
    ajax_load("pizza", get_filters(), function(input){
        add_table("Pizza", "15", pizza_table_head_tmpl, pizza_table_row_tmpl, input);
    });
}

function update_pizza_table(){
    ajax_load("pizza", get_filters(), function(input){
        console.log(input.length)
    });
}

function get_filters(){
    return {
        "base_style": JSON.stringify(get_filter("crusts")),
        "toppings": JSON.stringify(get_filter("toppings")),
        "diameter": JSON.stringify(get_num_filter("sizes")),
        "slices": JSON.stringify(get_num_filter("slices")),
    };
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

/* Helpers */

function ajax_load(func, args, callback, loader){
    if(loader == true)
        show_loader();
    return $.ajax({
        url: func,
        data: args
    }).done(function(input){
        if(loader == true)
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
