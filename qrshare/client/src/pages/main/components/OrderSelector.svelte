<script>
    import { ComboGroup } from "../../../components/list";
    import { isSorted } from "../store";

    const options = ["Relevance", "None"];
    let selected = options[0];

    function toggle(e) {
        const { option } = e.detail;

        /* clicked currently selected, skiiip */
        if (option === selected) return;

        isSorted.set(options[0] === option);
        selected = option;
    }
</script>

<label for="order-by">Order by</label>
<ComboGroup {options} {selected} on:toggle={toggle} />
