<script>
    import { SwitchGroup } from "../../../components/list";
    import { isSorted } from "../store";

    const options = ["Relevance", "None"];
    let selected = [true, false];

    function toggle(e) {
        const { index } = e.detail;

        /* clicked currently selected, skiiip */
        if (selected[index]) return;

        /* invert selected */
        selected = selected.map((v) => !v);

        /* since there is only one options, it either is or isnt
           and this code will only run it there is a change */
        isSorted.flip();
    }
</script>

<label for="order-by">Order by</label>
<SwitchGroup {options} {selected} on:toggle={toggle} />
