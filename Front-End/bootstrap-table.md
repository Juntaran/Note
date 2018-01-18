# bootstrap-table

``` html
<div class="container" style="width:1500px";>
{{/*<div class="table-responsive">*/}}
    <br>
    <br>
    <div id="toolbar">
        <button id="button" class="btn btn-default" onclick="javascrtpt:window.location.href='/admin'">返回</button>
    </div>
    <table id="table">
        <thead>
        <tr>
            <th data-field="Id"         data-sortable="true" data-align="center">ID</th>
            <th data-field="Name"       data-sortable="true" data-align="center">用户名</th>
        </tr>
        </thead>
    </table>
</div>


<script>
    var $table = $('#table'),
        $button = $('#button');
    $(function () {
        $table.bootstrapTable({
            url: "/history/provideHistoryTable",
            method: 'get',
            search: true,  //是否显示搜索框功能
            striped: true,  //是否显示行间隔色
            cache: false,    //是否使用缓存
            pagination: true,  //是否分页
            sidePagination: "client",           //分页方式
            pageNumber: 1,                      //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            sortable: true,  //是否启用排序
            showRefresh: true, //是否显示刷新功能
            showToggle: true,
            iconSize: 'outline',
            toolbar: '#exampleTableEventsToolbar', //可以在table上方显示的一条工具栏，
            icons: {
                refresh: 'glyphicon-repeat',
                toggle: 'glyphicon-list-alt',
            },
            sortName: 'Id',
            sortOrder: 'desc',
            formatLoadingMessage: function () {
                return "No Records";
            },
        });
        $('#button').click(function () {
            $table.bootstrapTable('refresh', {url: '/getTable'});
        });
    });

</script>
```

___

## Reference

* [bootstrap-table 官方文档](http://bootstrap-table.wenzhixin.net.cn/documentation/)