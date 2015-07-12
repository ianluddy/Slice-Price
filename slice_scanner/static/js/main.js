/* Constants */
var FADE = 300;
var TASK_DELAY = 800;

/* Globals */
var refresh_function = null;
var sort_by = "score";
var sort_dir = -1;
var page = 0;
var tasks = {};
var stats = {};
var page_title, page_main;
var pizza_info = {};
var vendor_info = [];
var title_tmpl, filter_group_tmpl, pizza_table_head_tmpl, pizza_table_row_tmpl, table_tmpl, table_page_tmpl,
    table_title_tmpl, spinner_tmpl, no_result_tmpl, pizza_grid_tmpl;

$(document).ready(function () {
    $(document).ajaxStart(function() { Pace.restart(); });
    ajax_load("stats", {}, update_counts);
    ajax_load("vendors", {}, function(input){vendor_info = input;});
    cache_elements();
    setInterval(run_tasks, TASK_DELAY);

    $.when(
        ajax_load('templates.html', {}, attach_templates)
    ).done(templates_loaded);
});

function run_tasks(){
    for( var func_id in tasks ){
        var task = tasks[func_id];
        if( task["stamp"] != undefined && task["stamp"] < Date.now() ){
            task["stamp"] = undefined;
            async(task["func"]);
        }
    }
}

function queue_task(func){
    tasks[func.name] = {
        "stamp": Date.now() + TASK_DELAY,
        "func": func
    }
}

function async(func){
    setTimeout(func, 0);
}

function templates_loaded(){
    attach_templates();
    compile_templates();
    add_tab_handlers();
}

function init_filters(){
    $(".sl-btn").on("click", function(){$(this).toggleClass("sl-btn-active")});
}

function init_checkboxes(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
}

function redraw_footable(){
    $('.footable').trigger('footable_redraw');
}

function init_footable(){
    $('.footable').footable();
}

function cache_elements(){
    page_main = $("#page_main");
    page_title = $("#page_title");
}

function compile_templates(){
    title_tmpl = Handlebars.compile($("#title_tmpl").html());
    filter_group_tmpl = Handlebars.compile($("#filter_group_tmpl").html());
    pizza_table_head_tmpl = Handlebars.compile($("#pizza_table_head_tmpl").html());
    pizza_table_row_tmpl = Handlebars.compile($("#pizza_table_row_tmpl").html());
    table_tmpl = Handlebars.compile($("#table_tmpl").html());
    table_page_tmpl = Handlebars.compile($("#table_page_tmpl").html());
    table_title_tmpl = Handlebars.compile($("#table_title_tmpl").html());
    spinner_tmpl = Handlebars.compile($("#spinner_tmpl").html());
    no_result_tmpl = Handlebars.compile($("#no_result_tmpl").html());
    pizza_grid_tmpl = Handlebars.compile($("#pizza_grid_tmpl").html());
}

function attach_templates(input){
    $("#tmpl_holder").html(input);
}

function add_tab_handlers(){
    $("#side-menu li.tab").on("click", function(){
        $(this).addClass("active").siblings().removeClass("active");
        clear();
        window[$(this).attr("target")]();
    });
    $("#side-menu li.tab").first().click();
}

function add_body_handlers(){
    $(".sl-btn").on("mouseout", function(){$(this).removeClass("focus").blur();});
}

function update_counts(input){
    stats = input;
    $("#pizza_cnt").text(input["pizza"]);
    $("#side_cnt").text(input["sides"]);
    $("#dessert_cnt").text(input["desserts"]);
    $("#drink_cnt").text(input["drinks"]);
    $("#combo_cnt").text(input["combos"]);
}

function get_table(){
    return $("#sl-table-wrapper");
}

function load_pizza_page(){
    show_loader(page_main, function(){
        $.when(
            ajax_load("pizza/bases", {}, function(input){pizza_info["bases"] = input;}),
            ajax_load("pizza/toppings", {}, function(input){pizza_info["toppings"] = input;}),
            ajax_load("pizza/styles", {}, function(input){pizza_info["styles"] = input;}),
            ajax_load("pizza/sizes", {}, function(input){pizza_info["sizes"] = input;}),
            ajax_load("pizza/diameters", {}, function(input){pizza_info["diameters"] = input;}),
            ajax_load("pizza/slices", {}, function(input){pizza_info["slices"] = input;})
        ).done(draw_pizza_page);
    });
}

function draw_pizza_page(){
    refresh_function = fetch_pizza;

    draw_table_template();

    // Add filters
    var filter_wrapper = $("#sl-filter-wrapper");
    remove_filter_handler();

    add_filter(filter_group_tmpl, filter_wrapper, "vendors", vendor_info, "danger", "btn-outline", "active");
    add_filter(filter_group_tmpl, filter_wrapper, "crusts", pizza_info["bases"], "warning", "btn-outline", "active");
    add_filter(filter_group_tmpl, filter_wrapper, "toppings", pizza_info["toppings"], "primary", "btn-outline", "");
    add_filter(filter_group_tmpl, filter_wrapper, "sizes", pizza_info["diameters"], "info", "btn-circle btn-outline", "active");
    add_filter(filter_group_tmpl, filter_wrapper, "slices", pizza_info["slices"], "info", "btn-circle btn-outline", "active");
    add_filter_handler(function(){queue_task(fetch_pizza)});
    // init_checkboxes();
    init_filters();

    // Add table
    // add_pizza_table();

    // add_body_handlers();

    hide_loader(page_main);
    add_sort_handlers();
    fetch_pizza();
}

function draw_table_template(){
    $(page_main).append(table_page_tmpl());
}

function add_filter(tmpl, dom, id, items, theme, style, active){
    $(dom).append(tmpl({
        "id": id,
        "title": id.toUpperCase(),
        "items": items,
        "theme": theme,
        "style": style,
        "active": active
    }));
    //    $(dom).find(".sl-btn").on("click", function(){$(this).toggleClass("sl-btn-active")});
}

function add_filter_handler(func){
    $("#sl-filter-wrapper").on("click.filter", ".sl-btn", func);
}

function remove_filter_handler(){
    $("#sl-filter-wrapper").off("click.filter", ".sl-btn");
}

function get_filter(id){
    var filtered = [];
    $("#" + id + " .sl-btn-active").each(function(){filtered.push($(this).attr("filter_id"))});
    if (filtered.length > 0)
        return filtered;
    return undefined;
}

function get_num_filter(id){
    var filtered = [];
    $("#" + id + " .sl-btn-active").each(function(){filtered.push(parseFloat($(this).attr("filter_id")))});
    if (filtered.length > 0)
        return filtered;
    return undefined;
}
//
//function add_table(title, page_size, head_tmpl, body_tmpl, data){
//    $("#sl-table-wrapper").append(table_tmpl({
//        "title": title,
//        "page_size": page_size,
//        "head": head_tmpl(),
//        "body": body_tmpl({"data": data})
//    }));
//    init_footable();
//    hide_loader(page_main);
//}

//function add_pizza_table(){
//    ajax_load("pizza", get_filters(), function(input){
//        add_table("Pizza", "10", pizza_table_head_tmpl, pizza_table_row_tmpl, input);
//    });
//}
//
//function update_table_header(items, item_count, vendor_count){
//    $("#table_title").html(table_title_tmpl({"item_count": item_count, "items": items, "vendor_count": vendor_count}))
//}

function fetch_pizza(){
    show_loader(get_table(), function(){
        ajax_load("pizza", fetch_pizza_parameters(), function(input){
            //update_table_header("Pizza(s)", input.length, get_filter("vendors").length);
            //update_table_contents(pizza_table_row_tmpl, {"data": input});
            get_table().empty().append(pizza_grid_tmpl({"items": input}));
            hide_loader(get_table());
        })
    });
}

function fetch_pizza_parameters(){
    return {
        "vendor": JSON.stringify(get_filter("vendors")),
        "base_style": JSON.stringify(get_filter("crusts")),
        "toppings": JSON.stringify(get_filter("toppings")),
        "diameter": JSON.stringify(get_num_filter("sizes")),
        "slices": JSON.stringify(get_num_filter("slices")),
        "page": page,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    };
}

function update_table_contents(tmpl, data){
    if( data.data.length < 1){
        $("#footable_head").hide();
        $("#footable_body").hide();
        $("#footable_footer").hide();
        if( $("#no_result").length == 0 )
            $("#table_wrapper .ibox-content").append(no_result_tmpl());
    }else{
        $("#no_result").remove();
        $("#footable_head").show();
        $("#footable_body").show();
        $("#footable_footer").show();
        $("#footable_body").html(tmpl(data));
        redraw_footable();
    }
}

function get_pizza_filters(){
    return {
        "vendors": JSON.stringify(get_filter("vendors")),
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

/* Sorting */

function add_sort_handlers(){
    $("#sl-sort-desc").on("click", sort_dir_handler);
    $("#sl-sort-asc").on("click", sort_dir_handler);
    $("#sl-sort-by li a").on("click", sort_by_handler);
}

function sort_by_handler(){
    var sort_value = $(this).text();
    sort_by = sort_value.toLowerCase();
    $("#sl-sorted-by-label").text(sort_value);
    refresh_data();
}

function sort_dir_handler(){
    $(this).addClass("btn-primary").removeClass("btn-white");
    $(this).siblings().addClass("btn-white").removeClass("btn-primary");
    sort_dir = $(this).attr("sort_dir");
    refresh_data();
}

/* Loading */

function refresh_data(){
    refresh_function();
}

function ajax_load(func, args, callback){
    return $.ajax({
        url: func,
        data: args
    }).done(function(input){
        if (callback)
            callback(input);
    });
}

function show_loader(dom, func){
    $(dom).animate({"opacity": 0.4}, FADE).append($(spinner_tmpl()).fadeIn(FADE));
    setTimeout(func, FADE);
}

function hide_loader(dom){
    setTimeout(function(){
        $(dom).animate({"opacity": 1}, FADE);
        $("#spinner").fadeOut(FADE, function(){$(this).remove()});
    });
}
