layui.define(['layer', 'form', 'laytpl'], function (exports) {
    "use strict";
    var areaList = ''
    let $ = layui.$
        , form = layui.form
        , layarea = {
        _id: 0
        , config: {}
        , set: function (options) {
            let that = this;
            that.config = $.extend({}, that.config, options);
            return that;
        }
        , on: function (events, callback) {
            return layui.onevent.call(this, 'layarea', events, callback);
        }
    }
        , thisArea = function () {
        let that = this;
        return {
            layarea: function (files) {
                that.layarea.call(that, files);
            }
            , config: that.config
        }
    }
        , Class = function (options) {
        let that = this;
        that.config = $.extend({}, that.config, layarea.config, options);
        that.render();
    };
    //

    //
    $.ajax({
        url: '',
        type: 'post',
        data: {
            // 'url':window.location.pathname
        },
        success: function (data) {
            // console.log(data.data);
            // alert(areaList)
            areaList = data.data;


            //     areaList = {
            //   province_list: {
            //     110000: '北京市',
            //     120000: '天津市',
            //     130000: '河北省',
            //     140000: '山西省',
            //     150000: '内蒙古自治区',
            //
            //     900000: '海外'
            //   },
            //   city_list: {
            //     110100: '北京市',
            //     120100: '天津市',
            //     130100: '石家庄市',
            //     130200: '唐山市',
            //     130300: '秦皇岛市',
            //     130400: '邯郸市',
            //     130500: '邢台市',
            //     130600: '保定市',
            //     130700: '张家口市',
            //
            //     984000: '美国'
            //   },
            //   county_list: {
            //     110101: '东城区',
            //     110102: '西城区',
            //     110105: '朝阳区',
            //     110106: '丰台区',
            //     110107: '石景山区',
            //     110108: '海淀区',
            //     110109: '门头沟区',
            //     110111: '房山区',
            //
            //   }
            // };


            Class.prototype.config = {
                elem: '',
                data: {
                    province: '--选择省--',
                    city: '--选择市--',
                    county: '--选择区--',
                },
                change: function (result) {
                }
            };

            Class.prototype.index = 0;

            Class.prototype.render = function () {
                let that = this, options = that.config;
                options.elem = $(options.elem);
                options.bindAction = $(options.bindAction);

                that.events();
            };

            Class.prototype.events = function () {
                let that = this, options = that.config, index;
                let provinceFilter = 'province-' + layarea._id;
                let cityFilter = 'city-' + layarea._id;
                let countyFilter = 'county-' + layarea._id;

                let provinceEl = options.elem.find('.province-selector');
                let cityEl = options.elem.find('.city-selector');
                let countyEl = options.elem.find('.county-selector');

                //filter
                if (provinceEl.attr('lay-filter')) {
                    provinceFilter = provinceEl.attr('lay-filter');
                }
                if (cityEl.attr('lay-filter')) {
                    cityFilter = cityEl.attr('lay-filter');
                }
                if (countyEl.attr('lay-filter')) {
                    countyFilter = countyEl.attr('lay-filter');
                }
                provinceEl.attr('lay-filter', provinceFilter);
                cityEl.attr('lay-filter', cityFilter);
                countyEl.attr('lay-filter', countyFilter);

                //获取默认值
                if (provinceEl.data('value')) {
                    options.data.province = provinceEl.data('value');
                }
                if (cityEl.data('value')) {
                    options.data.city = cityEl.data('value');
                }
                if (countyEl.data('value')) {
                    options.data.county = countyEl.data('value');
                }
                provinceEl.attr('lay-filter', provinceFilter);
                cityEl.attr('lay-filter', cityFilter);
                countyEl.attr('lay-filter', countyFilter);

                //监听结果
                form.on('select(' + provinceFilter + ')', function (data) {
                    options.data.province = data.value;
                    let code = getCode('province', data.value);
                    renderCity(code);

                    options.change(options.data);
                });
                form.on('select(' + cityFilter + ')', function (data) {
                    options.data.city = data.value;
                    let code = getCode('city', data.value);
                    renderCounty(code);

                    options.change(options.data);
                });
                form.on('select(' + countyFilter + ')', function (data) {
                    options.data.county = data.value;

                    options.change(options.data);
                });

                renderProvince();

                //查找province
                function renderProvince() {
                    let tpl = '';
                    let provinceList = getList("province");
                    let currentCode = '';
                    let currentName = '';
                    provinceList.forEach(function (_item) {
                        if (!currentCode) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        if (_item.name === options.data.province) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        tpl += '<option value="' + _item.name + '">' + _item.name + '</option>';
                    });
                    options.data.province = currentName;
                    provinceEl.html(tpl);
                    provinceEl.val(options.data.province);
                    form.render('select');
                    renderCity(currentCode);
                }

                function renderCity(provinceCode) {
                    let tpl = '';
                    let cityList = getList('city', provinceCode.slice(0, 2));
                    let currentCode = '';
                    let currentName = '';
                    cityList.forEach(function (_item) {
                        if (!currentCode) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        if (_item.name === options.data.city) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        tpl += '<option value="' + _item.name + '">' + _item.name + '</option>';
                    });
                    options.data.city = currentName;
                    cityEl.html(tpl);
                    cityEl.val(options.data.city);
                    form.render('select');
                    renderCounty(currentCode);
                }

                function renderCounty(cityCode) {
                    let tpl = '';
                    let countyList = getList('county', cityCode.slice(0, 4));
                    let currentCode = '';
                    let currentName = '';
                    countyList.forEach(function (_item) {
                        if (!currentCode) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        if (_item.name === options.data.county) {
                            currentCode = _item.code;
                            currentName = _item.name;
                        }
                        tpl += '<option value="' + _item.name + '">' + _item.name + '</option>';
                    });
                    options.data.county = currentName;
                    countyEl.html(tpl);
                    countyEl.val(options.data.county);

                    form.render('select');
                }

                function getList(type, code) {
                    let result = [];

                    if (type !== 'province' && !code) {
                        return result;
                    }

                    let list = areaList[type + "_list"] || {};
                    result = Object.keys(list).map(function (code) {
                        return {
                            code: code,
                            name: list[code]
                        };
                    });

                    if (code) {
                        // oversea code
                        if (code[0] === '9' && type === 'city') {
                            code = '9';
                        }

                        result = result.filter(function (item) {
                            return item.code.indexOf(code) === 0;
                        });
                    }

                    return result;
                }

                function getCode(type, name) {
                    let code = '';
                    let list = areaList[type + "_list"] || {};
                    layui.each(list, function (_code, _name) {
                        if (_name === name) {
                            code = _code;
                        }
                    });

                    return code;
                }
            };

            layarea.render = function (options) {
                let inst = new Class(options);
                layarea._id++;
                return thisArea.call(inst);
            };

            //暴露接口
            exports('layarea', layarea);

        }

    });


});