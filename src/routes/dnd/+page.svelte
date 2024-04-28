<script>
  // TODO: Modularizar
	// NOTE: Inspired by https://svelte.dev/repl/810b0f1e16ac4bbd8af8ba25d5e0deff?version=3.4.2.
	import {flip} from 'svelte/animate';
 

	let correct_answers = [
    {
      "id": "0",
      "answer": "Banana"
    },
    {
      "id": "1",
      "answer": "Apple",
    },
    {
      "id": "2",
      "answer": "Orange",
    },
  ];
	
  let user_answers = [
    {
      "id": "0",
      "answer": ""
    },
    {
      "id": "1",
      "answer": "",
    },
    {
      "id": "2",
      "answer": "",
    },
  ]

  let options = [...correct_answers]

	let hoveringOverBasket;
	
	function dragStart(event, ansIndex, location) {
		// The data we want to make available when the element is dropped
    // is the index of the item being dragged and
    // the index of the basket from which it is leaving.
    console.log(ansIndex)
		const data = {ansIndex, location};
   	event.dataTransfer.setData('text/plain', JSON.stringify(data));
	}
	
	function drop(event,indexPosition) {
		event.preventDefault();
    const json = event.dataTransfer.getData("text/plain");
		const {ansIndex, location} = JSON.parse(json);

    // dragging from options or user_answers?
    if (location === "options"){
//    NOTE: splice is like filter but changes original array
      let obj = options.splice(ansIndex,1)
      user_answers[indexPosition].answer = obj[0].answer
    } else {
      let ans = user_answers[ansIndex].answer
      user_answers[ansIndex].answer = user_answers[indexPosition].answer  
      user_answers[indexPosition].answer = ans 
    }
		// Remove the item from one basket.
		// Splice returns an array of the deleted elements, just one in this case.
		// const [item] = baskets[data.basketIndex].items.splice(data.itemIndex, 1);
    // if (location === "options"){
    // [correct_answers[ansIndex].answer, user_answers[i].answer] = [user_answers[i].answer, correct_answers[ansIndex].answer] 

    // } else {
      // [user_answers[ansIndex].answer, user_answers[ansIndex].answer] = [user_answers[ansIndex].answer, user_answers[ansIndex].answer] 
    // }
    // Add the item to the drop target basket.
    // NOTE: makes the array re-render
    options = options
		hoveringOverBasket = null;
	}
  // TODO: revisar q todo este bien y dar un mje
  // NOTE: no esta al reves la flag? 🤔 
  let flag = false;
  function revisar(){
    if (options.length !== 0){
      popover.showPopover()
      return
    }
    popover2.showPopover()
    return
  }

</script>

<div id="popover" popover>
    <p class="beef">Todavía no se completó todo!!!</p>
</div>

<div id="popover2" popover>
    <p class="beef text-8xl">Completaste todo 👍</p>
</div>
<div class="flex justify-between">
<h1 id="title">Draggear</h1>
  <button class="btn btn-neutral" on:click={revisar}>Revisar</button>
  </div>
<section class="border-white border border-solid p-4">
<h3>Respuestas</h3>
<hr>
<div id="asda" class="flex gap-8 min-h-40">
  {#each user_answers as answer, i (answer)}
    <ul animate:flip
	    on:dragenter={() => hoveringOverBasket = i}
	  	class:hovering={hoveringOverBasket === i}
      on:dragleave={() => hoveringOverBasket = null}
  		on:drop={event => drop(event,answer.id)}
  		ondragover="return false"

      class="border border-solid border-white-500 rounded-xl w-32 h-12">
        <li draggable={true} on:dragstart={event => dragStart(event, answer.id, "answers")}>
          {answer.answer}
        </li>
    </ul> 
  {/each}
</div>
</section>
<section class="border-white border-dashed border p-4 mt-4">
<h3>Opciones</h3>
<hr>
<div id="options" class="flex">
  {#each options as option, answerIndex (option)}
  <div animate:flip> <!-- an element that uses the animate directive must be in a keyed each block -->
    <ul>
        <div class="item">
        <li
          draggable={true}
          on:dragstart={event => dragStart(event, answerIndex, "options")}
        >
          {option.answer}
        </li>
      </div>
    </ul>
  </div>
{/each}
</div>
</section>
<style>
	.hovering {
		border-color: green;
	}
	.item {
		display: inline; /* required for flip to work */
    border-color: solid white 1px;
    border-radius: 8px;
    align-items: center;
	}

	li {
		cursor: pointer;
		display: inline-block;
		padding: 10px;
	}
	li:hover {
		background: orange;
		color: white;
	}
  ul {
		display: flex; /* required for drag & drop to work when .item display is inline */
    height: fit-content;
		min-height: 40px; /* needed when empty */
		padding: 10px;
    justify-content: center;
  }
</style>
