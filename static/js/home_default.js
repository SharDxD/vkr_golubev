function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function addRow(){
   /*  var bodyRef = document.getElementById('orders').getElementsByTagName('tbody')[0];
    var newRow = bodyRef.insertRow();

    for (var i = 0; i < 9; i++){
        var newCell = newRow.insertCell();
        newCell.contentEditable = "true";
    } */
    viewModel.items.push({id: "", name: "", category: "", num: "", weight: "", price: "", status: "", datetime: "", comment: ""});
}

function tableToJSON(){
    var myRows = [];
    var $headers = $("th");
    var $rows = $("tbody tr").each(function(index) {
        $cells = $(this).find("td");
        myRows[index] = {};
        $cells.each(function(cellIndex) {
            if ($($headers[cellIndex])[0].id == "id" || ($($headers[cellIndex])[0].id) == "category" || ($($headers[cellIndex])[0].id) == "price" || ($($headers[cellIndex])[0].id) == "num"){
                myRows[index][$($headers[cellIndex])[0].id] = Number($(this).html());     
            } 
            else myRows[index][$($headers[cellIndex])[0].id] = $(this).html();
        });    
    });
    var myObj = {};
    myObj.orders = myRows;
    return myObj
}
json = [{id: "", category: "", num: "", weight: "", price: "", status: "", datetime: "", comment: ""}]

var viewModel = {
    items: ko.observableArray(json)
};
var json = [];

$(document).ready(function () {
    ko.applyBindings(viewModel, document.getElementById("orders"));
});

$("#num_order_token").submit(function(e){
    e.preventDefault();
    
    var form = $(this);
    var formdata = getFormData(form);

    $.ajax({
        type: "GET",
        url: "https://eorder.auditory.ru/token_chk", /// URL API
        data: {
            token: formdata["token"],
        },
        success: function(data){
            $.ajax({
                type: "GET",
                url: "https://eorder.auditory.ru/order",
                data: {
                    order_id: formdata["order-number"],
                },
                success: function(data){
                    json = []
                    for (var i=0; i<data.number_of_rows;i++){
                        json.push({
                            id: i+1,
                            name: data[i+1].name,
                            category: data[i+1].category,
                            num: data[i+1].num,
                            weight: data[i+1].weight,
                            price: data[i+1].price,
                            status: data[i+1].status,
                            datetime: data[i+1].datetime,
                            comment: data[i+1].comment,
                        })
                    }
                    if (json.length == 0){
                        json = [{id: "", name: "", category: "", num: "", weight: "", price: "", status: "", datetime: "", comment: ""}]
                    }
                    viewModel.items(json);
                    document.getElementById("order").innerHTML = "Заказ №" + String(data.order_id)
                    document.title = "Заказ №" + String(data.order_id)
                },
                error: function(data){
                    alert("Заказа не существует!")
                } 
            })
        },
        error: function(data){
            if (data.responseJSON.Status_code == 401){
                alert("Токен неверный!")
            }
        }
    })
})

$("#change_table").submit(function(e){
    e.preventDefault();
    var form = $(this);
    var formdata = getFormData(form);

    $.ajax({
        type: "GET",
        url: "https://eorder.auditory.ru/token_chk",
        data: {
            token: formdata["token"],
        },
        success: function(data){
            if (data.Status_code == 200 && data.type >= 3){
                formatted_data = tableToJSON()
                ///formatted_data["order_id"] = Number(document.getElementById("order").innerHTML.slice(7))
                formatted_data["order_id"] = Number(document.getElementById("order-number").value)
                $.ajax({
                    type: "POST",
                    url: "https://eorder.auditory.ru/order", ///APIURL
                    data: JSON.stringify(formatted_data),
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function(data){
                        alert("Заказ изменен!")
                    },
                    error: function(data){
                        alert("Что-то пошло не так!")
                    }
                })
            }
            else alert("Недостасточно прав изменить заказ!")
        },
        error: function(data){
            alert("У вас нет доступа изменить заказ!")
        }
    })
})