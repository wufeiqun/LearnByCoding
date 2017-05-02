"use strict"

var data = [
	{
		id: "01",
		name: "item-1",
		checked: false
	},
	{
		id: "02",
		name: "item-2",
		checked: false,
		children: [
			{
				id: "02-01",
				name: "item-2-1",
				checked: false
			},
			{
				id: "02-02",
				name: "item-2-2",
				checked: false
			},
			{
				id: "02-03",
				name: "item-2-3",
				checked: false,
				children: [
					{
						id: "02-03-01",
						name: "item-2-3-1",
						checked: false
					},
					{
						id: "02-03-02",
						name: "item-2-3-2",
						checked: false,
						children: [
							{
								id: "02-03-02-01",
								name: "item-2-3-2-1",
								checked: false
							}
						]
					}
				]
			},
		]
	}
];

var checkedList = ["02", "02-02", "02-03-02-01"];


function iterArr(data) {
	for (let i = 0; i<data.length; i++) {
		// console.log(data[i]["id"]);
		if (checkedList.indexOf(data[i]["id"]) !== -1) {
			data[i]["checked"] = true;
		}
		if ("children" in data[i]) {
			iterArr(data[i]["children"]);
		} 
	}
}

iterArr(data);