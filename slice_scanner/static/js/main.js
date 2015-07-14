/* Constants */
var FADE = 500;
var TASK_DELAY = 800;

/* Globals */
var fetch_function = null;
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
    ajax_load("stats", {}, update_counts);
    ajax_load("vendors", {}, function(input){vendor_info = input;});
    page_main = $("#page_main");
    page_title = $("#page_title");
    setInterval(run_tasks, TASK_DELAY);
    toaster("Welcome!", "Use the filters to find your ideal Pizza!");

    $.when(
        ajax_load('templates.html', {}, attach_templates)
    ).done(templates_loaded);
});

/* Pizza */

function load_pizza_page(){
    show_loader(page_main, function(){
        $.when(
            ajax_load("pizza/bases", {}, function(input){pizza_info["bases"] = input;}),
            ajax_load("pizza/toppings", {}, function(input){pizza_info["toppings"] = input;}),
            ajax_load("pizza/styles", {}, function(input){pizza_info["styles"] = input;}),
            ajax_load("pizza/sizes", {}, function(input){pizza_info["sizes"] = input;}),
            ajax_load("pizza/diameters", {}, function(input){pizza_info["diameters"] = input;}),
            ajax_load("pizza/slices", {}, function(input){pizza_info["slices"] = input;})
        ).done(function(){ draw_product_page(add_pizza_filters, fetch_pizza) });
    });
}

function add_pizza_filters(){
    add_filter(filter_group_tmpl, "vendors", vendor_info, "danger", "btn-outline", "active");
    add_filter(filter_group_tmpl, "crusts", pizza_info["bases"], "warning", "btn-outline", "active");
    add_filter(filter_group_tmpl, "toppings", pizza_info["toppings"], "primary", "btn-outline", "");
    add_filter(filter_group_tmpl, "sizes", pizza_info["diameters"], "info", "btn-circle btn-outline", "active");
    add_filter(filter_group_tmpl, "slices", pizza_info["slices"], "info", "btn-circle btn-outline", "active");
}

function fetch_pizza(){
    fetch("pizza", fetch_pizza_parameters, pizza_grid_tmpl);
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

/* Templates */

function templates_loaded(){
    attach_templates();
    compile_templates();
    add_tab_handlers();
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

/* Filters */

function add_filter(tmpl, id, items, theme, style, active){
    $(get_filter_wrapper()).append(tmpl({
        "id": id,
        "title": id.toUpperCase(),
        "items": items,
        "theme": theme,
        "style": style,
        "active": active
    }));
}

function init_filters() {
    $(".sl-btn").on("click", function () {
        $(this).toggleClass("sl-btn-active")
    });
}

function add_filter_handler(){
    $(get_filter_wrapper()).on("click.filter", ".sl-btn", function(){queue_task(fetch_function)});
}

function remove_filter_handler(){
    $(get_filter_wrapper()).off("click.filter", ".sl-btn");
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

/* Page */

function add_tab_handlers(){
    $("#side-menu li.tab").on("click", function(){
        $(this).addClass("active").siblings().removeClass("active");
        clear();
        window[$(this).attr("target")]();
    });
    $("#side-menu li.tab").first().click();
}

function update_counts(input){
    stats = input;
    $("#pizza_cnt").text(input["pizza"]);
    $("#side_cnt").text(input["sides"]);
    $("#dessert_cnt").text(input["desserts"]);
    $("#drink_cnt").text(input["drinks"]);
    $("#combo_cnt").text(input["combos"]);
}

function draw_product_page(add_filters, fetcher){
    fetch_function = fetcher;
    $(page_main).append(table_page_tmpl());
    remove_filter_handler();
    add_filters();
    add_filter_handler();
    init_filters();
    hide_loader(page_main);
    add_sort_handlers();
    fetcher();
    $(document).ajaxStart(function() { Pace.restart(); });
}

function no_result(){
    get_table_wrapper().empty().append(no_result_tmpl());
}

function clear(){
    $(page_title).empty();
    $(page_main).empty();
}

function get_table_wrapper(){
    return $("#sl-table-wrapper");
}

function get_filter_wrapper(){
    return $("#sl-filter-wrapper");
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

function fetch(endpoint, param_func, template){
    show_loader(get_table_wrapper(), function(){
        ajax_load(endpoint, param_func(), function(input){
            if( input.length > 0 ){
                get_table_wrapper().empty().append(template({"items": input}));
            }else{
                no_result();
            }
            hide_loader(get_table_wrapper());
        })
    });
}

function refresh_data(){
    fetch_function();
}

function ajax_load(func, args, callback){
    return $.ajax({
        url: func,
        data: args
    }).done(function(input){
        //console.log(input);
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

/* Notifications */

function toaster(title, message){
    setTimeout(function() {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            showMethod: 'slideDown',
            timeOut: 4000
        };
        toastr.info(message, title);
    }, 1300);
}

/* Task Manager */

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