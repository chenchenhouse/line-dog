def flex_message():
    message = FlexSendMessage
    (
            alt_text = '陳陳的嘉理',
            contents = 
    {
    "type": "bubble",
    "hero": 
    {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": 
        {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "url": "https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png"
    },
    "body": 
    {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "action": 
        {
        "type": "uri",
        "uri": "https://linecorp.com"
        },
        "contents": 
        [
        {
            "type": "text",
            "text": "陳陳的嘉理",
            "size": "xxl",
            "weight": "bold",
            "align": "center",
            "margin": "none",
            "action": 
            {
            "type": "uri",
            "label": "action",
            "uri": "https://chenchenhouse.com//"
            }
        },
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": 
            [
            {
                "type": "box",
                "layout": "baseline",
                "contents": 
                [
                {
                    "type": "icon",
                    "url": "https://png.pngtree.com/element_our/png_detail/20181227/stock-market-vector-icon-png_294394.jpg",
                    "size": "lg",
                    "margin": "none",
                    "offsetBottom": "none",
                    "offsetTop": "sm"
                },
                {
                    "type": "text",
                    "text": "股市報你知",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "action": 
                    {
                    "type": "uri",
                    "label": "action",
                    "uri": "https://chenchenhouse.com/category/sstock/"
                    },
                    "color": "#8A8A00"
                },
                {
                    "type": "text",
                    "size": "sm",
                    "align": "end",
                    "color": "#0000C6",
                    "text": "財經"
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": 
                [
                {
                    "type": "icon",
                    "url": "https://steamcode.com.tw/img/device.png",
                    "size": "xl",
                    "margin": "none",
                    "offsetTop": "sm",
                    "offsetBottom": "none",
                    "offsetStart": "none"
                },
                {
                    "type": "text",
                    "text": "程式交易",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "size": "md",
                    "color": "#8A8A00",
                    "action": 
                    {
                    "type": "uri",
                    "label": "action",
                    "uri": "https://chenchenhouse.com/category/program_transaction/"
                    }
                },
                {
                    "type": "text",
                    "text": "資訊",
                    "size": "sm",
                    "align": "end",
                    "color": "#0000C6"
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": 
                [
                {
                    "type": "icon",
                    "url": "https://img.ixintu.com/download/jpg/20200718/9f93ffebc5ffdfe32c08de65fcfb8ec6_512_512.jpg!bg",
                    "size": "xl",
                    "margin": "none",
                    "offsetTop": "sm",
                    "offsetBottom": "none",
                    "offsetStart": "none"
                },
                {
                    "type": "text",
                    "text": "美食愛分享",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "size": "md",
                    "color": "#8A8A00"
                },
                {
                    "type": "text",
                    "text": "食記",
                    "size": "sm",
                    "align": "end",
                    "color": "#0000C6"
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": 
                [
                {
                    "type": "icon",
                    "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTL7jrrEUwqGbejfBH7lhHzUCAoYP3QZJkEgw&usqp=CAU",
                    "size": "xl",
                    "margin": "none",
                    "offsetTop": "sm",
                    "offsetBottom": "none",
                    "offsetStart": "none"
                },
                {
                    "type": "text",
                    "text": "好書推薦",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "size": "md",
                    "color": "#8A8A00"
                },
                {
                    "type": "text",
                    "text": "財經",
                    "size": "sm",
                    "align": "end",
                    "color": "#0000C6"
                }
                ]
            }
            ]
        },
        {
            "type": "text",
            "text": "#股票#程式#大數據#美食",
            "wrap": True,
            "color": "#F75000",
            "size": "xxs"
        }
        ]
    },
    "footer": 
    {
        "type": "box",
        "layout": "vertical",
        "contents": 
        [
        {
            "type": "button",
            "style": "primary",
            "color": "#844200",
            "action": 
            {
            "type": "uri",
            "label": "馬上觀看",
            "uri": "https://chenchenhouse.com//"
            },
            "margin": "none"
        }
        ]
    }
    }
    )
    return message