Number.prototype.formatMoney = function(c, d, t) {
    var n = this,
        c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? '.' : d,
        t = t == undefined ? ',' : t,
        s = n < 0 ? '-' : '',
        i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + '',
        j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, '$1' + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : '');
};

$(document).ready(function() {

    console.log('Document ready');
    


    $(".nav-sidebar li a[href^='#']").on('click', function(e) {
        console.log('TEST');
        // prevent default anchor click behavior
        e.preventDefault();

        // store hash
        $('.nav-sidebar li').removeClass('active');
        var hash = this.hash;
        $(this).parent().addClass('active');

        // animate
        $('html, body').animate({
            scrollTop: $(this.hash).offset().top - 60
        }, 300, function() {


            // when done, add hash to url
            // (default click behaviour)
            window.location.hash = hash;
        });

    }); //end nav element selector




    // Remove the formatting to get integer data for summation
    var intVal = function(i) {
        return typeof i === 'string' ?
            i.replace(/[\$,]/g, '') * 1 :
            typeof i === 'number' ?
            i : 0;
    };

    var table = $('#recent_sales_table').DataTable({
        'paging': false,
        'order': [
            [7, 'desc']
        ]
    });

    var get_average = function(x) {
        var sum_prices = 0;
        var arrayLength = x.length;
        for (var i = 0; i < arrayLength; i++) {
            sum_prices += intVal(x[i][2]);
        }
        average_price = (sum_prices / arrayLength).formatMoney(0, '.', ',');

        //catch if there is no data for this
        if (average_price !== average_price) {
            average_price = 'na';
        }

        return average_price;
    };
    var tabled = $('#recent_sales_table').DataTable();
    $('#recent_sales_table tbody').on('click', 'tr', function() {
        $(this).toggleClass('active');
        console.log(tabled.rows('.active').data().length + ' row(s) selected');
        selected_items = tabled.rows('.active').data();
        all_items = tabled.rows().data();
        footer_sel_val = get_average(selected_items);
        footer_all_val = get_average(all_items);
        $($('#recent_sales_table').dataTable().api().column(2).footer()).html(
            'Average for ' + selected_items.length + ' selected homes: $' + footer_sel_val + '<br>(Overall average: $' + footer_all_val + ')'
        );
        $('#recent_sales_est').text(footer_sel_val);
    });
    
    //select first three rows
    $('#recent_sales_table tbody').children('tr:lt(3)').click();

}); //end document.ready

$('#tagtest').tagsinput({
    typeahead: {
        local: ['Carpet flooring - new', 'Hardwood flooring - New', 'Walls  - Stained', 'Walls - Freshly Painted', 'Natural lighting', 'Water damage', 'Fireplace - gas',
            'Fireplace - woodburning', 'Stairs - creeky', 'Closet - walk-in', 'Closet - his/hers', 'Granite counters in kitchen', 'Stainless steel appliances in kitchen',
            'Island kitchen', 'Eating area or breakfast nook', 'Basement - finished', 'Basement - not enough head room', 'Basement - signs of water damage', 'Garage -1 car',
            'Garage - 2 car', 'Garage - 3 car', 'Driveway - cracked', 'Garage - finished', 'Roof - needs replacing', 'Roof - no signs of leakage, discoloration',
            'Siding - brick', 'Siding - Vinyl', 'Siding - Wood', 'Siding - Aluminum', 'Windows - insulated', 'Windows - need replacing', 'Outdoor - landscaping',
            'Outdoor - swimming pool', 'Outdoor - garden', 'Outdoor - Wood deck', 'Outdoor - patio', 'Outdoor - lack of privacy', 'City view', 'Nature view',
            'Signs of pests', 'Good curb appeal', 'Exterior - good paint job', 'Exterior - Attractive landscaping', 'Exterior - Fence', 'Furnace - needs replacing',
            'Air Conditioning - needs replacing', 'Bathrooms - Renovated', 'Bathrooms - Need renovation', 'High ceilings', 'Loft', 'High noise level', 'Quiet',
            'East facing', 'central A/C', 'No central heating', 'Eat-in kitchen', 'Hardwood floors under carpet', 'Exterior: Auto sprinkler system', 'Single story', 'Remodeled', 'Shed',
            'Tennis court'
        ]
    }
});

var tagtest = function(event, current_est_price) {

    console.log('Increase value 10');
    $('#eazy_estimate').animate({
        color: '#fff',
        opacity: '0.5'
    }, 400);
    $('#eazy_estimate').text('EazyHouz Estimate: $ ' +
        (current_est_price + 10000 * $('#tagtest').tagsinput('items').length).formatMoney(0, '.', ',')
    );
    $('#eazy_estimate').animate({
        color: '#333',
        opacity: '1'
    }, 400);
};

