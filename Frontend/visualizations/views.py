from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
import sys, os
import json

def article_hypertree(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []
    context = {'data': data}
    return render(request, 'visualizations/article_hypertree.html', context)

def article_hypertree_js(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = {
            "id": "347_0",
            "name": "Nine Inch Nails",
            "children": [{
                "id": "126510_1",
                "name": "Jerome Dillon",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "52163_2",
                    "name": "Howlin' Maggie",
                    "data": {
                        "band": "Jerome Dillon",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "324134_3",
                    "name": "nearLY",
                    "data": {
                        "band": "Jerome Dillon",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }, {
                "id": "173871_4",
                "name": "Charlie Clouser",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235952_5",
                "name": "James Woolley",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235951_6",
                "name": "Jeff Ward",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235950_11",
                "name": "Richard Patrick",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "1007_12",
                    "name": "Filter",
                    "data": {
                        "band": "Richard Patrick",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "327924_13",
                    "name": "Army of Anyone",
                    "data": {
                        "band": "Richard Patrick",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }, {
                "id": "2396_14",
                "name": "Trent Reznor",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "3963_15",
                    "name": "Pigface",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "32247_16",
                    "name": "1000 Homo DJs",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "83761_17",
                    "name": "Option 30",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "133257_18",
                    "name": "Exotic Birds",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }],
            "data": []
            }

    data = json.dumps(data)
    context = {'data': data}
    return render(request, 'visualizations/article_hypertree_js.html', context)

def article_spacetree(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []
    context = {'data': data}
    return render(request, 'visualizations/article_spacetree.html', context)

def article_spacetree_js(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = {
                "id": "node02",
                "name": "0.2",
                "data": {},
                "children": [{
                    "id": "node13",
                    "name": "1.3",
                    "data": {},
                    "children": [{
                        "id": "node24",
                        "name": "2.4",
                        "data": {},
                        "children": [{
                            "id": "node35",
                            "name": "3.5",
                            "data": {},
                            "children": [{
                                "id": "node46",
                                "name": "4.6",
                                "data": {},
                                "children": []
                            }]
                        }, {
                            "id": "node37",
                            "name": "3.7",
                            "data": {},
                            "children": [{
                                "id": "node48",
                                "name": "4.8",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node49",
                                "name": "4.9",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node410",
                                "name": "4.10",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node411",
                                "name": "4.11",
                                "data": {},
                                "children": []
                            }]
                        }, {
                            "id": "node312",
                            "name": "3.12",
                            "data": {},
                            "children": [{
                                "id": "node413",
                                "name": "4.13",
                                "data": {},
                                "children": []
                            }]
                        }, {
                            "id": "node314",
                            "name": "3.14",
                            "data": {},
                            "children": [{
                                "id": "node415",
                                "name": "4.15",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node416",
                                "name": "4.16",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node417",
                                "name": "4.17",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node418",
                                "name": "4.18",
                                "data": {},
                                "children": []
                            }]
                        }, {
                            "id": "node319",
                            "name": "3.19",
                            "data": {},
                            "children": [{
                                "id": "node420",
                                "name": "4.20",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node421",
                                "name": "4.21",
                                "data": {},
                                "children": []
                            }]
                        }]
                    }, {
                        "id": "node2138",
                        "name": "2.138",
                        "data": {},
                        "children": [{
                            "id": "node3139",
                            "name": "3.139",
                            "data": {},
                            "children": [{
                                "id": "node4140",
                                "name": "4.140",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node4141",
                                "name": "4.141",
                                "data": {},
                                "children": []
                            }]
                        }, {
                            "id": "node3142",
                            "name": "3.142",
                            "data": {},
                            "children": [{
                                "id": "node4143",
                                "name": "4.143",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node4144",
                                "name": "4.144",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node4145",
                                "name": "4.145",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node4146",
                                "name": "4.146",
                                "data": {},
                                "children": []
                            }, {
                                "id": "node4147",
                                "name": "4.147",
                                "data": {},
                                "children": []
                            }]
                        }]
                    }]
                }]
            };

    data = json.dumps(data)
    context = {'data': data}
    return render(request, 'visualizations/article_spacetree_js.html', context)

def tweet_hypertree(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []
    context = {'data': data}
    return render(request, 'visualizations/tweet_hypertree.html', context)

def tweet_hypertree_js(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = {
            "id": "347_0",
            "name": "Nine Inch Nails",
            "children": [{
                "id": "126510_1",
                "name": "Jerome Dillon",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "52163_2",
                    "name": "Howlin' Maggie",
                    "data": {
                        "band": "Jerome Dillon",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "324134_3",
                    "name": "nearLY",
                    "data": {
                        "band": "Jerome Dillon",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }, {
                "id": "173871_4",
                "name": "Charlie Clouser",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235952_5",
                "name": "James Woolley",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235951_6",
                "name": "Jeff Ward",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "235950_11",
                "name": "Richard Patrick",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "1007_12",
                    "name": "Filter",
                    "data": {
                        "band": "Richard Patrick",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "327924_13",
                    "name": "Army of Anyone",
                    "data": {
                        "band": "Richard Patrick",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }, {
                "id": "2396_14",
                "name": "Trent Reznor",
                "data": {
                    "band": "Nine Inch Nails",
                    "relation": "member of band"
                },
                "children": [{
                    "id": "3963_15",
                    "name": "Pigface",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "32247_16",
                    "name": "1000 Homo DJs",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "83761_17",
                    "name": "Option 30",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }, {
                    "id": "133257_18",
                    "name": "Exotic Birds",
                    "data": {
                        "band": "Trent Reznor",
                        "relation": "member of band"
                    },
                    "children": []
                }]
            }],
            "data": []
            }

    data = json.dumps(data)
    context = {'data': data}
    return render(request, 'visualizations/tweet_hypertree_js.html', context)
