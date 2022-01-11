let d = document

d.querySelectorAll("input[type=radio]").forEach(r => {
	r.onclick = evt => {
		// let elt = d.getElementById("log")
		// let log = elt.value.split(",")
		// log.push(r.value)
		// elt.value = log.join(",")
		// console.log(elt.value)
		d.forms[0].submit()
	}
})

