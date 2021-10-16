init_values = () => {
    N.val(1000)
    i0.val(1)
    r0.val(0)
    betta.val(1)
    gamma.val(1)
    block_size.val(10)
    epsilon.val(0.01)
    max_iter.val(10)
}
actualize_values = () => {
    $("#label_N").text(N.val())
    $("#label_i0").text(i0.val())
    $("#label_r0").text(r0.val())
    $("#label_betta").text(betta.val())
    $("#label_gamma").text(gamma.val())
    $("#label_block_size").text(block_size.val())
    $("#label_epsilon").text(epsilon.val())
    $("#label_max_iter").text(max_iter.val())
}
create_plot = () => {
    $.ajax({
        url: "/",
        type: "POST",
        data: {
            N: N.val(),
            I0: i0.val(),
            R0: r0.val(),
            betta: betta.val(),
            gamma: gamma.val(),
            block_size: block_size.val(),
            epsilon: epsilon.val(),
            max_iter: max_iter.val()
        }
    }).done((data) => {
        let trace1 = {
            x: data.t,
            y: data.S,
            type: 'line',
            name: "Susceptibles",
        }
        let trace2 = {
            x: data.t,
            y: data.R,
            type: 'line',
            name: "Removed",
        }
        let trace3 = {
            x: data.t,
            y: data.I,
            type: 'line',
            name: "Infected"
        }
        let layout = {
            autosize: true
        };
        let config = {
            displayModeBar: false,
        };
        Plotly.react('plot', {
            data: [trace1, trace2, trace3],
            layout: layout,
            config: config
        })
    })
}
special_actualization = () => {
    if(N.val() < parseInt(i0.val()) + parseInt(r0.val())){
        N.val(parseInt(i0.val()) + parseInt(r0.val()))
    }
}

var form = $(".formulario")
var N = $("#N")
var i0 = $("#I0")
var r0 = $("#R0")
var betta = $("#betta")
var gamma = $("#gamma")
var block_size = $("#block_size")
var epsilon = $("#epsilon")
var max_iter = $("#max_iter")

init_values()
actualize_values()
create_plot()

form.on("change", () => { 
    special_actualization()
    actualize_values() 
    create_plot()
})