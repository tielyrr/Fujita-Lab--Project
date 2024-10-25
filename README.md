# Fujita-Lab--Project
Updated summation of the work completed for the Fujita Lab at the University of Texas at Arlington in the Summer of 2024. Reference for any PhD students looking to replicate or modify any methods.

Contact info for any questions: tyler.dixon.b@gmail.com

### Purpose and Goals
- Create an automatically updating MySQL database for all complete, annotated, and chromosome-level Squamate genomes from NCBI.
- Use the database as a method for analyzing GC content among different parts of each chromosome, and among species.

### Why Study GC Content in Squamates?
Our DNA, made of 'Adenine - Thymine' and 'Cytosine - Guanine' pairs, is constantly mutating due to replication errors and environmental factors. Mutation is the basis for all variety and responsible for the diverse life we have on Earth. When we have mutations, there is a phenomenon called 'mutation bias' that preferentially converts GC -> AT (transversion). Evolutionary biologists are interested in the mechanism of maintinence of GC content in genomes and why mutation bias hasn't eliminated G's and C's altogether. So far, it has been found that gene density and GC content are positively correllated, that GC content is more involved in gene expression than AT, and that areas of recombination have higher GC content and consequently experience stronger selection.
Studying Squamates is of interest to the Fujita Lab because the Green Anole (Squamate), upon sequencing, was found to have less variability in GC content than other vertebrates. This suggests there may be a novel relationship in Squamates to maintain GC content. Our goals are to study diversity of GC content in Squamates amongst themselves, and in relation to vertebrates

## Data
### .gff Files
- Text data organized line-by-line, around 0.1GB in size. Consists of annotations for its respective FNA: string coordinates, IDs and various other information for all identified genes, chromosomes, exons, etc.
### .fna Files
- Text data organized line-by-line, around 2GB in size. Consists of a line to describe each chromosome or scaffold, then the sequence in successive lines of 80 characters.

We dealt with 21 genomes.

## Summary of work
### MySQL Database Design
In the folder 'SQL' you will find the files that show the database script, the model file, and the stored procedures we used to analyze the data. 

[U<html>
  <meta charset='utf-8'>
  
  <head>
      <style>
        body {
  font-family: -apple-system, BlinkMacSystemFont, Segoe WPC, Segoe UI, HelveticaNeue-Light, Ubuntu, Droid Sans,
    sans-serif;
  font-size: 14px;
  /* font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
	  'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
	  sans-serif; 
	  */
  -webkit-font-smoothing: auto;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
}

.horizontal-split-handle {
  background-color: var(--theme-border);
  width: var(--dim-splitter-thickness);
  cursor: col-resize;
}
.horizontal-split-handle:hover {
  background-color: var(--theme-bg-2);
}

.vertical-split-handle {
  background-color: var(--theme-border);
  height: var(--dim-splitter-thickness);
  cursor: row-resize;
}
.vertical-split-handle:hover {
  background-color: var(--theme-bg-2);
}

.icon-invisible {
  visibility: hidden;
}
.space-between {
  display: flex;
  justify-content: space-between;
}
.flex {
  display: flex;
}
.flexcol {
  display: flex;
  flex-direction: column;
}
.nowrap {
  white-space: nowrap;
}
.noselect {
  user-select: none;
}
.bold {
  font-weight: bold;
}
.flex1 {
  flex: 1;
}
.relative {
  position: relative;
}

.col-10 {
  flex-basis: 83.3333%;
  max-width: 83.3333%;
}
.col-9 {
  flex-basis: 75%;
  max-width: 75%;
}
.col-8 {
  flex-basis: 66.6667%;
  max-width: 66.6667%;
}
.col-7 {
  flex-basis: 58.3333%;
  max-width: 58.3333%;
}
.col-6 {
  flex-basis: 50%;
  max-width: 50%;
}
.col-5 {
  flex-basis: 41.6667%;
  max-width: 41.6667%;
}
.col-4 {
  flex-basis: 33.3333%;
  max-width: 33.3333%;
}
.col-3 {
  flex-basis: 25%;
  max-width: 25%;
}
.col-2 {
  flex-basis: 16.6666%;
  max-width: 16.6666%;
}

.largeFormMarker input[type='text'] {
  width: 100%;
  padding: 10px 10px;
  font-size: 14px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid var(--theme-border);
}

.largeFormMarker input[type='password'] {
  width: 100%;
  padding: 10px 10px;
  font-size: 14px;
  box-sizing: border-box;
  border-radius: 4px;
}

.largeFormMarker select {
  width: 100%;
  padding: 10px 10px;
  font-size: 14px;
  box-sizing: border-box;
  border-radius: 4px;
}

body *::-webkit-scrollbar {
  height: 0.8em;
  width: 0.8em;
}
body *::-webkit-scrollbar-track {
  border-radius: 1px;
  background-color: var(--theme-bg-1);
}
body *::-webkit-scrollbar-corner {
  border-radius: 1px;
  background-color: var(--theme-bg-2);
}

body *::-webkit-scrollbar-thumb {
  border-radius: 1px;
  background-color: var(--theme-bg-3);
}

body *::-webkit-scrollbar-thumb:hover {
  background-color: var(--theme-bg-4);
}

input {
  background-color: var(--theme-bg-0);
  color: var(--theme-font-1);
  border: 1px solid var(--theme-border);
}

input[disabled] {
  background-color: var(--theme-bg-1);
}

select {
  background-color: var(--theme-bg-0);
  color: var(--theme-font-1);
  border: 1px solid var(--theme-border);
}

select[disabled] {
  background-color: var(--theme-bg-1);
}

textarea {
  background-color: var(--theme-bg-0);
  color: var(--theme-font-1);
  border: 1px solid var(--theme-border);
}

.ace_gutter-cell.ace-gutter-sql-run {
  background-repeat: no-repeat;
  background-position: 2px center;

  /* content: '▶';
  margin-right: 3px; */

  /* border-radius: 20px 0px 0px 20px; */
  /* Change the color of the breakpoint if you want 
  box-shadow: 0px 0px 1px 1px #248c46 inset;  */
}

.theme-type-light .ace_gutter-cell.ace-gutter-sql-run {
  background-image: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTguMS4xLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIKCSB2aWV3Qm94PSIwIDAgMTcuODA0IDE3LjgwNCIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTcuODA0IDE3LjgwNDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxnIGlkPSJjOThfcGxheSI+CgkJPHBhdGggZmlsbD0nIzQ0NCcgZD0iTTIuMDY3LDAuMDQzQzIuMjEtMC4wMjgsMi4zNzItMC4wMDgsMi40OTMsMC4wODVsMTMuMzEyLDguNTAzYzAuMDk0LDAuMDc4LDAuMTU0LDAuMTkxLDAuMTU0LDAuMzEzCgkJCWMwLDAuMTItMC4wNjEsMC4yMzctMC4xNTQsMC4zMTRMMi40OTIsMTcuNzE3Yy0wLjA3LDAuMDU3LTAuMTYyLDAuMDg3LTAuMjUsMC4wODdsLTAuMTc2LTAuMDQKCQkJYy0wLjEzNi0wLjA2NS0wLjIyMi0wLjIwNy0wLjIyMi0wLjM2MVYwLjQwMkMxLjg0NCwwLjI1LDEuOTMsMC4xMDcsMi4wNjcsMC4wNDN6Ii8+Cgk8L2c+Cgk8ZyBpZD0iQ2FwYV8xXzc4XyI+Cgk8L2c+CjwvZz4KPC9zdmc+Cg==);
}

.theme-type-dark .ace_gutter-cell.ace-gutter-sql-run {
  background-image: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTguMS4xLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIKCSB2aWV3Qm94PSIwIDAgMTcuODA0IDE3LjgwNCIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTcuODA0IDE3LjgwNDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxnIGlkPSJjOThfcGxheSI+CgkJPHBhdGggZmlsbD0nI2RkZCcgZD0iTTIuMDY3LDAuMDQzQzIuMjEtMC4wMjgsMi4zNzItMC4wMDgsMi40OTMsMC4wODVsMTMuMzEyLDguNTAzYzAuMDk0LDAuMDc4LDAuMTU0LDAuMTkxLDAuMTU0LDAuMzEzCgkJCWMwLDAuMTItMC4wNjEsMC4yMzctMC4xNTQsMC4zMTRMMi40OTIsMTcuNzE3Yy0wLjA3LDAuMDU3LTAuMTYyLDAuMDg3LTAuMjUsMC4wODdsLTAuMTc2LTAuMDQKCQkJYy0wLjEzNi0wLjA2NS0wLjIyMi0wLjIwNy0wLjIyMi0wLjM2MVYwLjQwMkMxLjg0NCwwLjI1LDEuOTMsMC4xMDcsMi4wNjcsMC4wNDN6Ii8+Cgk8L2c+Cgk8ZyBpZD0iQ2FwYV8xXzc4XyI+Cgk8L2c+CjwvZz4KPC9zdmc+Cg==);
}

.ace_gutter-cell.ace-gutter-sql-run:hover {
   background-color: var(--theme-bg-2);
}

.ace_gutter-cell.ace-gutter-current-part {
   /* background-color: var(--theme-bg-2); */
   font-weight: bold;
   color: var(--theme-font-hover);
}
.logo.svelte-8utz2r{display:flex;margin-bottom:1rem;align-items:center;justify-content:center}.img.svelte-8utz2r{width:80px}.text.svelte-8utz2r{position:fixed;top:1rem;left:1rem;font-size:30pt;font-family:monospace;color:var(--theme-bg-2);text-transform:uppercase}.submit.svelte-8utz2r{margin:var(--dim-large-form-margin);display:flex}.submit.svelte-8utz2r input{flex:1;font-size:larger}.root.svelte-8utz2r{color:var(--theme-font-1);display:flex;justify-content:center;background-color:var(--theme-bg-1);align-items:baseline;position:fixed;top:0;left:0;right:0;bottom:0}.box.svelte-8utz2r{width:600px;max-width:80vw;border:1px solid var(--theme-border);border-radius:4px;background-color:var(--theme-bg-0)}.wrap.svelte-8utz2r{margin-top:20vh}.heading.svelte-8utz2r{text-align:center;margin:1em;font-size:xx-large}.root.svelte-11u34pp{color:var(--theme-font-1)}.title.svelte-11u34pp{font-size:x-large;margin-top:20vh;text-align:center}.error.svelte-11u34pp{margin-top:1em;text-align:center}.button.svelte-11u34pp{display:flex;justify-content:center;margin-top:1em}.root.svelte-1efqwi5{color:var(--theme-font-1)}.iconbar.svelte-1efqwi5{position:fixed;display:flex;left:0;top:var(--dim-header-top);bottom:var(--dim-statusbar-height);width:var(--dim-widget-icon-size);background:var(--theme-bg-inv-1)}.statusbar.svelte-1efqwi5{position:fixed;background:var(--theme-bg-statusbar-inv);height:var(--dim-statusbar-height);left:0;right:0;bottom:0;display:flex}.leftpanel.svelte-1efqwi5{position:fixed;top:var(--dim-header-top);left:var(--dim-widget-icon-size);bottom:var(--dim-statusbar-height);width:var(--dim-left-panel-width);background-color:var(--theme-bg-1);display:flex}.commads.svelte-1efqwi5{position:fixed;top:var(--dim-header-top);left:var(--dim-widget-icon-size)}.toolbar.svelte-1efqwi5{position:fixed;top:var(--dim-toolbar-top);height:var(--dim-toolbar-height);left:0;right:0;background:var(--theme-bg-1)}.splitter.svelte-1efqwi5{position:absolute;top:var(--dim-header-top);bottom:var(--dim-statusbar-height);left:calc(var(--dim-widget-icon-size) + var(--dim-left-panel-width))}.snackbar-container.svelte-1efqwi5{position:fixed;right:0;bottom:var(--dim-statusbar-height)}.titlebar.svelte-1efqwi5{position:fixed;top:0;left:0;right:0;height:var(--dim-titlebar-height)}.not-supported.svelte-1efqwi5{display:none}@media only screen and (max-width: 600px){.dbgate-screen.svelte-1efqwi5:not(.isElectron){display:none}.not-supported.svelte-1efqwi5:not(.isElectron){display:block}}.not-supported.svelte-1efqwi5{text-align:center}.big-icon.svelte-1efqwi5{font-size:20pt}.tabs-container.svelte-1efqwi5{position:fixed;top:var(--dim-header-top);left:var(--dim-content-left);bottom:var(--dim-statusbar-height);right:0;background-color:var(--theme-bg-1)}div.svelte-pa7e1d{position:fixed;left:-1000px;top:-1000px;visibility:hidden}td.svelte-pa7e1d{display:flex}.container.svelte-1s05410{display:flex;align-items:center;margin-right:10px}.spinner.svelte-1s05410{font-size:20pt;margin:10px}.wrapper.svelte-1s05410{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-around}.box.svelte-1s05410{background-color:var(--theme-bg-2);padding:10px;border:1px solid var(--theme-border)}.lds-ellipsis.svelte-45vupj.svelte-45vupj{display:inline-block;position:relative;width:80px;height:80px}.lds-ellipsis.svelte-45vupj div.svelte-45vupj{position:absolute;top:33px;width:13px;height:13px;border-radius:50%;background:#000;animation-timing-function:cubic-bezier(0, 1, 1, 0)}.lds-ellipsis.svelte-45vupj div.svelte-45vupj:nth-child(1){left:8px;animation:svelte-45vupj-lds-ellipsis1 0.6s infinite}.lds-ellipsis.svelte-45vupj div.svelte-45vupj:nth-child(2){left:8px;animation:svelte-45vupj-lds-ellipsis2 0.6s infinite}.lds-ellipsis.svelte-45vupj div.svelte-45vupj:nth-child(3){left:32px;animation:svelte-45vupj-lds-ellipsis2 0.6s infinite}.lds-ellipsis.svelte-45vupj div.svelte-45vupj:nth-child(4){left:56px;animation:svelte-45vupj-lds-ellipsis3 0.6s infinite}@keyframes svelte-45vupj-lds-ellipsis1{0%{transform:scale(0)}100%{transform:scale(1)}}@keyframes svelte-45vupj-lds-ellipsis3{0%{transform:scale(1)}100%{transform:scale(0)}}@keyframes svelte-45vupj-lds-ellipsis2{0%{transform:translate(0, 0)}100%{transform:translate(24px, 0)}}.starting-dbgate.svelte-45vupj.svelte-45vupj{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-around}.inner-flex.svelte-45vupj.svelte-45vupj{display:flex;align-items:center;flex-direction:column}.root.svelte-ks0vy{position:absolute;left:0;top:0;right:0;bottom:0}.icons-wrapper.svelte-ks0vy{position:absolute;right:5px;font-size:20pt;top:0;bottom:0;display:flex;align-items:center;display:flex}.icon-button.svelte-ks0vy{color:var(--theme-font-2);cursor:pointer}.icon-button.svelte-ks0vy:hover{color:var(--theme-font-1)}.tabs.svelte-ks0vy{height:var(--dim-tabs-panel-height);display:flex;overflow-x:auto;position:absolute;left:0;top:0;right:35px;bottom:0}.tabs.can-split.svelte-ks0vy{right:60px}.tabs.svelte-ks0vy::-webkit-scrollbar{height:7px}.db-group.svelte-ks0vy{display:flex;flex:1;align-content:stretch}.db-wrapper.svelte-ks0vy{display:flex;flex-direction:column;align-items:stretch}.db-name.svelte-ks0vy{display:flex;text-align:center;font-size:8pt;border-bottom:1px solid var(--theme-border);border-right:1px solid var(--theme-border);cursor:pointer;user-select:none;padding:1px;position:relative;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.db-name-inner.svelte-ks0vy{justify-content:center;flex-grow:1}.db-name.selected.svelte-ks0vy{background-color:var(--theme-bg-0)}.file-tab-item.svelte-ks0vy{border-right:1px solid var(--theme-border);border-bottom:2px solid var(--theme-border);padding-left:15px;padding-right:15px;flex-shrink:1;flex-grow:1;min-width:10px;display:flex;align-items:center;cursor:pointer;user-select:none}.file-tab-item.selected.svelte-ks0vy{background-color:var(--theme-bg-0)}.file-name.svelte-ks0vy{margin-left:5px;white-space:nowrap;flex-grow:1}.tab-group-buttons.svelte-ks0vy{margin-left:5px;margin-right:5px;color:var(--theme-font-3);display:flex}.tab-group-button.svelte-ks0vy:hover{color:var(--theme-font-1)}input.svelte-n46s8k{border:1px solid var(--theme-bg-button-inv-2);padding:5px;margin:2px;width:100px;background-color:var(--theme-bg-button-inv);color:var(--theme-font-inv-1);border-radius:2px}input.svelte-n46s8k:hover:not(.disabled){background-color:var(--theme-bg-button-inv-2)}input.svelte-n46s8k:active:not(.disabled){background-color:var(--theme-bg-button-inv-3)}input.disabled.svelte-n46s8k{background-color:var(--theme-bg-button-inv-3);color:var(--theme-font-inv-3)}.obj-heading.svelte-2dwto4{font-size:20px;margin:5px;margin-top:20px}.dbname.svelte-2dwto4{color:var(--theme-font-3)}.content.svelte-nk47x3{flex:1;display:flex;flex-direction:column;overflow-y:auto;overflow-x:hidden}span.svelte-143q17x{font-weight:bold}.heading.svelte-19ddf77{font-size:20px;margin:5px;margin-left:var(--dim-large-form-margin);margin-top:var(--dim-large-form-margin)}.themes.svelte-19ddf77{overflow-x:scroll;display:flex}.editor.svelte-19ddf77{position:relative;height:200px;width:400px;margin-left:var(--dim-large-form-margin)}.target.svelte-1d5rlxt{position:fixed;display:flex;top:0;left:0;right:0;bottom:0;background:var(--theme-bg-selected);align-items:center;justify-content:space-around;z-index:1000}.icon.svelte-1d5rlxt{display:flex;justify-content:space-around;font-size:50px;margin-bottom:20px}.info.svelte-1d5rlxt{display:flex;justify-content:space-around;margin-top:10px}.title.svelte-1d5rlxt{font-size:30px;display:flex;justify-content:space-around}.class-button.svelte-1d5rlxt{position:fixed;top:20px;right:20px;font-size:14pt;cursor:pointer}.wrapper.svelte-1a6igp5{display:flex;align-items:center}.icon.svelte-1a6igp5{margin-right:10px;font-size:20pt}pre.svelte-1a6igp5{max-height:calc(100vh - 300px);overflow-y:auto}.messages.svelte-1vzii1g{height:30vh;display:flex}.container.svelte-1qj7qwd{display:flex;user-select:none;align-items:stretch;height:var(--dim-toolbar-height)}.root.svelte-1qj7qwd{display:flex;align-items:stretch;justify-content:space-between}.activeTab.svelte-1qj7qwd{background-color:var(--theme-bg-2);white-space:nowrap;display:flex;padding-left:15px;padding-right:15px}.activeTabInner.svelte-1qj7qwd{align-self:center}.wrapper.svelte-1nclm36{font-size:23pt;height:60px;display:flex;align-items:center;justify-content:center;color:var(--theme-font-inv-2)}.wrapper.svelte-1nclm36:hover{color:var(--theme-font-inv-1)}.wrapper.selected.svelte-1nclm36{color:var(--theme-font-inv-1);background:var(--theme-bg-inv-3)}.main.svelte-1nclm36{display:flex;flex:1;flex-direction:column}.main.svelte-1kyrubd{width:500px;background:var(--theme-bg-2)}.mainInner.svelte-1kyrubd{padding:5px}.content.svelte-1kyrubd{max-height:400px;overflow-y:scroll}.search.svelte-1kyrubd{display:flex}input.svelte-1kyrubd{width:100%}.command.svelte-1kyrubd{padding:5px;display:flex;justify-content:space-between}.command.svelte-1kyrubd:hover{background:var(--theme-bg-3)}.command.selected.svelte-1kyrubd{background:var(--theme-bg-selected)}.shortcut.svelte-1kyrubd{background:var(--theme-bg-3)}.pages.svelte-1kyrubd{display:flex}.page.svelte-1kyrubd{padding:5px;border:1px solid var(--theme-border);cursor:pointer}.page.svelte-1kyrubd:hover{color:var(--theme-font-hover)}.page.selected.svelte-1kyrubd{background:var(--theme-bg-1)}.main.svelte-as4084{display:flex;color:var(--theme-font-inv-15);align-items:stretch;justify-content:space-between;cursor:default;flex:1}.container.svelte-as4084{display:flex;align-items:stretch}.item.svelte-as4084{padding:0px 10px;display:flex;align-items:center;white-space:nowrap}.version.svelte-as4084{max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.clickable.svelte-as4084{cursor:pointer}.clickable.svelte-as4084:hover{background-color:var(--theme-bg-statusbar-inv-hover)}.colorbox.svelte-as4084{padding:0px 3px;border-radius:2px;color:var(--theme-bg-statusbar-inv-font);background:var(--theme-bg-statusbar-inv-bg)}.wrapper.svelte-7p89xz{width:400px;border:1px solid var(--theme-border);background-color:var(--theme-bg-2);margin:10px;position:relative}.message.svelte-7p89xz{margin:10px}.close.svelte-7p89xz{position:absolute;right:5px;top:5px;cursor:pointer}.close.svelte-7p89xz:hover{color:var(--theme-font-hover)}.buttons.svelte-7p89xz{display:flex;justify-content:flex-end}.button.svelte-7p89xz{margin:5px}.container.svelte-1sw5v4y{-webkit-app-region:drag;user-select:none;height:var(--dim-titlebar-height);display:flex;align-items:center;background:var(--theme-bg-2);color:var(--theme-font-1)}.title.svelte-1sw5v4y{flex-grow:1;text-align:center}.icon.svelte-1sw5v4y{padding:5px}.button.svelte-1sw5v4y{padding:5px 10px;font-size:14pt}.button.svelte-1sw5v4y:hover{background:var(--theme-bg-hover)}.close-button.svelte-1sw5v4y:hover{background:var(--theme-icon-red)}.menu.svelte-1sw5v4y{margin-left:10px;-webkit-app-region:no-drag}.actions.svelte-1sw5v4y{display:flex;margin-left:0;-webkit-app-region:no-drag}.tabs.svelte-685oc7{position:absolute;top:0;left:0;height:var(--dim-tabs-panel-height);right:0;background-color:var(--theme-bg-1);border-top:1px solid var(--theme-border)}.content.svelte-685oc7{position:absolute;top:var(--dim-tabs-panel-height);left:0;bottom:0;right:0;background-color:var(--theme-bg-1)}.outer.svelte-qjn8rh{flex:1;position:relative}.inner.svelte-qjn8rh{overflow:scroll;position:absolute;left:0;top:0;right:0;bottom:0}.padLeft.svelte-1p2qnn1{margin-left:0.25rem}.padRight.svelte-1p2qnn1{margin-right:0.25rem}.outer.svelte-1dacrl4{--bg-1:var(--theme-bg-1);--bg-2:var(--theme-bg-3);background:linear-gradient(to bottom, var(--bg-1) 5%, var(--bg-2) 100%);background-color:var(--bg-1);border:1px solid var(--bg-2);display:inline-block;cursor:pointer;vertical-align:middle;color:var(--theme-font-1);font-size:12px;padding:3px;margin:0;text-decoration:none;display:flex}.narrow.svelte-1dacrl4{padding:3px 1px}.outer.disabled.svelte-1dacrl4{color:var(--theme-font-3)}.outer.svelte-1dacrl4:hover:not(.disabled){border:1px solid var(--theme-font-1)}.outer.svelte-1dacrl4:active:not(.disabled){background:linear-gradient(to bottom, var(--bg-2) 5%, var(--bg-1) 100%);background-color:var(--bg-2)}.inner.svelte-1dacrl4{margin:auto;flex:1;text-align:center}.square.svelte-1dacrl4{width:18px}.label.svelte-2e9efj{margin-bottom:3px;color:var(--theme-font-3)}.checkLabel.svelte-2e9efj{cursor:default;user-select:none}.largeFormMarker.svelte-2e9efj:not(.noMargin){margin:var(--dim-large-form-margin)}.disabled.svelte-2e9efj{color:var(--theme-font-3)}.close-button.svelte-1y2o65v{margin-left:5px;color:var(--theme-font-3)}.close-button.svelte-1y2o65v:hover{color:var(--theme-font-1)}.container.svelte-16cskqp{flex:1;display:flex;position:absolute;left:0;right:0;top:0;bottom:0}.child1.svelte-16cskqp{display:flex;position:relative;overflow:hidden}.child2.svelte-16cskqp{flex:1;display:flex;position:relative;overflow:hidden}.collapse.svelte-16cskqp{position:absolute;bottom:16px;height:40px;width:16px;background:var(--theme-bg-2);display:flex;flex-direction:column;justify-content:center;z-index:100}.collapse.svelte-16cskqp:hover{color:var(--theme-font-hover);background:var(--theme-bg-3);cursor:pointer}.button.svelte-1nx9a1b{padding:5px 15px;color:var(--theme-font-1);border:1px solid var(--theme-border);width:120px;height:60px;background-color:var(--theme-bg-1)}.button.fillHorizontal.svelte-1nx9a1b{width:auto;margin:0px 10px}.button.svelte-1nx9a1b:not(.disabled):hover{background-color:var(--theme-bg-2)}.button.svelte-1nx9a1b:not(.disabled):active{background-color:var(--theme-bg-3)}.button.disabled.svelte-1nx9a1b{color:var(--theme-font-3)}.icon.svelte-1nx9a1b{font-size:30px;text-align:center}.inner.svelte-1nx9a1b{text-align:center}input.svelte-nsxrdb{flex:1;min-width:10px;min-height:22px;width:10px;border:none}.row.svelte-9r8t4s{margin:5px}.label.svelte-9r8t4s{margin-bottom:3px;color:var(--theme-font-3)}.checkLabel.svelte-9r8t4s{cursor:default;user-select:none}.disabled.svelte-9r8t4s{color:var(--theme-font-3)}.value.svelte-9r8t4s{margin-left:15px;margin-top:3px}div.svelte-7wgwlv{display:flex;border-bottom:1px solid var(--theme-border);margin-bottom:5px}.hidden.svelte-d62x0y{display:none}.main-container.svelte-d62x0y{position:relative;flex:1;flex-direction:column;user-select:none}.main-container.svelte-d62x0y:not(.hidden){display:flex}.wrapper.svelte-184i6gf{overflow:hidden;position:relative;flex-direction:column;display:flex}.bglayer.svelte-rfjhvl{position:fixed;z-index:1;left:0;top:0;width:100%;height:100%;overflow:auto;background-color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0.4)}.window.svelte-rfjhvl{background-color:var(--theme-bg-0);border:1px solid var(--theme-border);overflow:auto;outline:none}.window.svelte-rfjhvl:not(.fullScreen):not(.simple){border-radius:10px;margin:auto;margin-top:15vh;width:50%}.window.fullScreen.svelte-rfjhvl{position:fixed;top:0;left:0;right:0;bottom:0}.window.simple.svelte-rfjhvl{margin:auto;margin-top:25vh;width:30%}.close.svelte-rfjhvl{font-size:12pt;padding:5px 10px;border-radius:10px}.close.svelte-rfjhvl:hover{background-color:var(--theme-bg-2)}.header.svelte-rfjhvl{font-size:15pt;padding:15px;display:flex;justify-content:space-between;background-color:var(--theme-bg-modalheader)}.header.fullScreen.svelte-rfjhvl{border-bottom:1px solid var(--theme-border)}.content.svelte-rfjhvl:not(.fullScreen){border-bottom:1px solid var(--theme-border);border-top:1px solid var(--theme-border)}.content.svelte-rfjhvl:not(.noPadding):not(.fullScreen){padding:15px}.content.fullScreen.svelte-rfjhvl{display:flex;position:fixed;top:60px;left:0;right:0;bottom:100px}.footer.svelte-rfjhvl:not(.fullScreen){border-bottom:1px solid var(--theme-border);padding:15px;background-color:var(--theme-bg-modalheader)}.footer.fullScreen.svelte-rfjhvl{position:fixed;height:100px;left:0;right:0;bottom:0px;border-top:1px solid var(--theme-border);background-color:var(--theme-bg-modalheader)}div.svelte-3may20{flex:1 1;overflow-x:auto;overflow-y:auto;width:var(--dim-left-panel-width)}div.svelte-1msuoss{padding:5px;font-weight:bold;text-transform:uppercase;background-color:var(--theme-bg-1);border:2px solid var(--theme-border)}div.clickable.svelte-1msuoss:hover{background-color:var(--theme-bg-2)}.container.svelte-a39cm2{display:flex;margin-right:10px;align-items:center}.icon.svelte-a39cm2{font-size:20pt;margin:10px}.container-small.svelte-a39cm2{display:flex;margin-right:10px}.container.svelte-kqh1iu{flex:1;display:flex;position:absolute;left:0;right:0;top:0;bottom:0;flex-direction:column}.child1.svelte-kqh1iu{display:flex;position:relative;overflow:hidden}.child2.svelte-kqh1iu{flex:1;display:flex;position:relative;overflow:hidden}.collapse.svelte-kqh1iu{position:absolute;right:16px;width:40px;height:16px;background:var(--theme-bg-2);display:flex;justify-content:center;z-index:100}.collapse.svelte-kqh1iu:hover{color:var(--theme-font-hover);background:var(--theme-bg-3);cursor:pointer}.arrow.svelte-tc4cku{font-size:30px;color:var(--theme-icon-blue);align-self:center}.title.svelte-tc4cku{font-size:20px;text-align:center;margin:10px 0px}a.svelte-1gj6vtf{text-decoration:none;cursor:pointer;color:var(--theme-font-link)}a.svelte-1gj6vtf:hover{text-decoration:underline}.main.svelte-1tav8z1{display:flex;flex-direction:column;overflow:auto}.main.flex1.svelte-1tav8z1{flex:1}.tabs.svelte-1tav8z1{display:flex;height:var(--dim-tabs-height);right:0;background-color:var(--theme-bg-2)}.tab-item.svelte-1tav8z1{border-right:1px solid var(--theme-border);padding-left:15px;padding-right:15px;display:flex;align-items:center;cursor:pointer}.tab-item.selected.svelte-1tav8z1{background-color:var(--theme-bg-1)}.content-container.svelte-1tav8z1{flex:1;position:relative}.container.svelte-1tav8z1:not(.isInline){position:absolute;display:flex;left:0;right:0;top:0;bottom:0}.container.svelte-1tav8z1:not(.tabVisible):not(.isInline){visibility:hidden}.container.isInline.svelte-1tav8z1:not(.tabVisible){display:none}.select.svelte-3jbx4l{--border:1px solid var(--theme-border);--placeholderColor:var(--theme-font-2);--background:var(--theme-bg-0);--listBackground:var(--theme-bg-1);--itemActiveBackground:var(--theme-bg-selected);--itemIsActiveBG:var(--theme-bg-selected);--itemHoverBG:var(--theme-bg-hover);--itemColor:var(--theme-font-1);--listEmptyColor:var(--theme-bg-0);--multiClearBG:var(--theme-bg-3);--multiClearFill:var(--theme-font-2);--multiClearHoverBG:var(--theme-bg-hover);--multiClearHoverFill:var(--theme-font-hover);--multiItemActiveBG:var(--theme-bg-1);--multiItemActiveColor:var(--theme-font-1);--multiItemBG:var(--theme-bg-1);--multiItemDisabledHoverBg:var(--theme-bg-1);--multiItemDisabledHoverColor:var(--theme-bg-1)}.ace-container.svelte-14wuf0i{position:absolute;left:0;top:0;right:0;bottom:0}.container.svelte-1uijirt{position:relative;height:150px;width:200px;min-height:150px;min-width:200px;margin:10px;cursor:pointer}.iconbar-settings-modal.svelte-1uijirt{position:absolute;display:flex;flex-direction:column;align-items:center;left:0;top:0;bottom:0;width:30px;background:var(--theme-bg-inv-1);color:var(--theme-font-inv-2)}.titlebar-settings-modal.svelte-1uijirt{left:0;top:0;right:0;height:10px;background:var(--theme-bg-2)}.content.svelte-1uijirt{position:absolute;display:flex;left:30px;top:10px;bottom:0;right:0;background:var(--theme-bg-1);display:flex;align-items:center;justify-content:center;color:var(--theme-font-1)}.current.svelte-1uijirt{font-weight:bold}.icon.svelte-1uijirt{margin:5px 0px}.main.svelte-1klg37t.svelte-1klg37t{padding:5px;cursor:pointer;white-space:nowrap;font-weight:normal}.main.svelte-1klg37t.svelte-1klg37t:hover{background-color:var(--theme-bg-hover)}.isBold.svelte-1klg37t.svelte-1klg37t{font-weight:bold}.status.svelte-1klg37t.svelte-1klg37t{margin-left:5px}.ext-info.svelte-1klg37t.svelte-1klg37t{font-weight:normal;margin-left:5px;color:var(--theme-font-3)}.expand-icon.svelte-1klg37t.svelte-1klg37t{margin-right:3px}.pin.svelte-1klg37t.svelte-1klg37t{float:right;color:var(--theme-font-2)}.pin.svelte-1klg37t.svelte-1klg37t:hover{color:var(--theme-font-hover)}.main.svelte-1klg37t .pin.svelte-1klg37t{visibility:hidden}.main.svelte-1klg37t:hover .pin.svelte-1klg37t{visibility:visible}.unpin.svelte-1klg37t.svelte-1klg37t{float:right;color:var(--theme-font-2)}.unpin.svelte-1klg37t.svelte-1klg37t:hover{color:var(--theme-font-hover)}.pin-active.svelte-1klg37t.svelte-1klg37t{float:right;color:var(--theme-font-2)}.wrapper.svelte-1lvmq5c{flex:1;display:flex;flex-direction:column}.main.svelte-1lvmq5c{display:flex;flex:1;flex-direction:column}.toolbar.svelte-1lvmq5c{display:flex;background:var(--theme-bg-1);align-items:center;border-bottom:1px solid var(--thene-border);margin:2px}.data.svelte-1lvmq5c{display:flex;flex:1;position:relative}div.svelte-3h7mlk{position:absolute;left:0;top:0;right:0;bottom:0;display:flex}.tabVisible.svelte-3h7mlk{visibility:visible}.svelte-3h7mlk:not(.tabVisible){visibility:hidden}.button.svelte-ygrxja{padding-left:15px;padding-right:15px;color:var(--theme-font-1);border:0;border-right:1px solid var(--theme-border);align-self:stretch;display:flex;user-select:none}.button.disabled.svelte-ygrxja{color:var(--theme-font-3)}.button.svelte-ygrxja:hover:not(.disabled){background:var(--theme-bg-2)}.button.svelte-ygrxja:active:hover:not(.disabled){background:var(--theme-bg-3)}.icon.svelte-ygrxja{margin-right:5px;color:var(--theme-font-link)}.icon.disabled.svelte-ygrxja{color:var(--theme-font-3)}.inner.svelte-ygrxja{white-space:nowrap;align-self:center}img.svelte-ygrxja{width:20px;height:20px}ul.svelte-3j24if{position:absolute;list-style:none;background-color:var(--theme-bg-0);border-radius:4px;border:1px solid var(--theme-border);box-shadow:0 6px 12px rgba(0, 0, 0, 0.175);padding:5px 0;margin:2px 0 0;font-size:14px;text-align:left;min-width:160px;z-index:1050;cursor:default;white-space:nowrap;overflow-y:auto;max-height:calc(100% - 20px)
  }.keyText.svelte-3j24if{font-style:italic;font-weight:bold;text-align:right;margin-left:16px}a.svelte-3j24if{padding:3px 20px;line-height:1.42;white-space:nop-wrap;color:var(--theme-font-1);display:flex;justify-content:space-between}a.disabled.svelte-3j24if{color:var(--theme-font-3)}a.svelte-3j24if:hover:not(.disabled){background-color:var(--theme-bg-1);text-decoration:none;color:var(--theme-font-1)}.divider.svelte-3j24if{margin:9px 0px 9px 0px;border-top:1px solid var(--theme-border);border-bottom:1px solid var(--theme-bg-0)}.menu-right.svelte-3j24if{position:relative;left:15px}.container.svelte-1beafpb{display:flex}.item.svelte-1beafpb{height:var(--dim-titlebar-height);padding:0px 10px;display:flex;align-items:center}.item.svelte-1beafpb:hover{background:var(--theme-bg-3)}.item.opened.svelte-1beafpb{background:var(--theme-bg-3)}.theme-type-dark ul.svelte-1l14734{--json-tree-string-color:#ffc5c5;--json-tree-symbol-color:#ffc5c5;--json-tree-boolean-color:#b6c3ff;--json-tree-function-color:#b6c3ff;--json-tree-number-color:#bfbdff;--json-tree-label-color:#e9aaed;--json-tree-arrow-color:#d4d4d4;--json-tree-null-color:#dcdcdc;--json-tree-undefined-color:#dcdcdc;--json-tree-date-color:#dcdcdc}ul.svelte-1l14734{--string-color:var(--json-tree-string-color, #cb3f41);--symbol-color:var(--json-tree-symbol-color, #cb3f41);--boolean-color:var(--json-tree-boolean-color, #112aa7);--function-color:var(--json-tree-function-color, #112aa7);--number-color:var(--json-tree-number-color, #3029cf);--label-color:var(--json-tree-label-color, #871d8f);--arrow-color:var(--json-tree-arrow-color, #727272);--null-color:var(--json-tree-null-color, #8d8d8d);--undefined-color:var(--json-tree-undefined-color, #8d8d8d);--date-color:var(--json-tree-date-color, #8d8d8d);--li-identation:var(--json-tree-li-indentation, 1em);--li-line-height:var(--json-tree-li-line-height, 1.3);--li-colon-space:0.3em;font-size:var(--json-tree-font-size, 12px);font-family:var(--json-tree-font-family, monospace)}ul.svelte-1l14734 li{line-height:var(--li-line-height);display:var(--li-display, list-item);list-style:none;white-space:nowrap}ul.svelte-1l14734,ul.svelte-1l14734 ul{padding:0;margin:0}ul.isDeleted.svelte-1l14734{background:var(--theme-bg-volcano);background-image:url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAEElEQVQImWNgIAX8x4KJBAD+agT8INXz9wAAAABJRU5ErkJggg==');background-repeat:repeat-x;background-position:50% 50%}ul.isModified.svelte-1l14734{background:var(--theme-bg-gold)}ul.isInserted.svelte-1l14734{background:var(--theme-bg-green)}.theme-dark{--theme-font-1:#e3e3e3;--theme-font-2:#b5b5b5;--theme-font-3:#888888;--theme-font-4:#5a5a5a;--theme-font-hover:#8dcff8;--theme-font-link:#65b7f3;--theme-font-alt:#b2e58b;--theme-bg-0:#111;--theme-bg-1:#333;--theme-bg-2:#4d4d4d;--theme-bg-3:#676767;--theme-bg-4:#818181;--theme-bg-alt:#111d2c;--theme-bg-gold:#443111;--theme-bg-orange:#442a11;--theme-bg-green:#1d3712;--theme-bg-volcano:#441d12;--theme-bg-red:#431418;--theme-bg-blue:#15395b;--theme-bg-magenta:#551c3b;--theme-font-inv-1:#ffffff;--theme-font-inv-15:#dedede;--theme-font-inv-2:#b3b3b3;--theme-font-inv-3:#808080;--theme-font-inv-4:#4d4d4d;--theme-bg-inv-1:#222;--theme-bg-inv-2:#3c3c3c;--theme-bg-inv-3:#565656;--theme-bg-inv-4:#707070;--theme-border:#555;--theme-bg-hover:#112a45;--theme-bg-selected:#15395b;--theme-bg-selected-point:#1765ad;--theme-bg-statusbar-inv:#0050b3;--theme-bg-statusbar-inv-hover:#096dd9;--theme-bg-statusbar-inv-font:#222;--theme-bg-statusbar-inv-bg:#ccc;--theme-bg-modalheader:rgb(43, 60, 61);--theme-bg-button-inv:#004488;--theme-bg-button-inv-2:#1a5794;--theme-bg-button-inv-3:#346aa0;--theme-icon-blue:#3c9ae8;--theme-icon-green:#8fd460;--theme-icon-red:#e84749;--theme-icon-gold:#e8b339;--theme-icon-yellow:#e8d639;--theme-icon-magenta:#e0529c;--theme-icon-inv-green:#8fd460;--theme-icon-inv-red:#e84749}.theme-light{--theme-font-1:#262626;--theme-font-2:#4d4d4d;--theme-font-3:#808080;--theme-font-4:#b3b3b3;--theme-font-hover:#061178;--theme-font-link:#10239e;--theme-font-alt:#135200;--theme-bg-0:#fff;--theme-bg-1:#ededed;--theme-bg-2:#d4d4d4;--theme-bg-3:#bbbbbb;--theme-bg-4:#a2a2a2;--theme-bg-alt:#f0f5ff;--theme-bg-gold:#fff1b8;--theme-bg-orange:#ffe7ba;--theme-bg-green:#d9f7be;--theme-bg-volcano:#ffd8bf;--theme-bg-red:#ffccc7;--theme-bg-blue:#91d5ff;--theme-bg-magenta:#ffadd2;--theme-font-inv-1:#ffffff;--theme-font-inv-15:#dedede;--theme-font-inv-2:#b3b3b3;--theme-font-inv-3:#808080;--theme-font-inv-4:#4d4d4d;--theme-bg-inv-1:#222;--theme-bg-inv-2:#3c3c3c;--theme-bg-inv-3:#565656;--theme-bg-inv-4:#707070;--theme-border:#ccc;--theme-bg-hover:#bae7ff;--theme-bg-selected:#91d5ff;--theme-bg-selected-point:#40a9ff;--theme-bg-statusbar-inv:#0050b3;--theme-bg-statusbar-inv-hover:#096dd9;--theme-bg-statusbar-inv-font:#222;--theme-bg-statusbar-inv-bg:#ccc;--theme-bg-modalheader:#eff;--theme-bg-button-inv:#337ab7;--theme-bg-button-inv-2:#4d8bc0;--theme-bg-button-inv-3:#679cc9;--theme-icon-blue:#096dd9;--theme-icon-green:#237804;--theme-icon-red:#cf1322;--theme-icon-gold:#d48806;--theme-icon-yellow:#d4b106;--theme-icon-magenta:#c41d7f;--theme-icon-inv-green:#8fd460;--theme-icon-inv-red:#e84749}.group.svelte-1a3znv3{user-select:none;padding:5px;cursor:pointer;white-space:nowrap;font-weight:bold}.group.svelte-1a3znv3:hover{background-color:var(--theme-bg-hover)}.expand-icon.svelte-1a3znv3{margin-right:3px}.subitems.svelte-k6fdqm{margin-left:28px}.editor.svelte-1jlkcxq{position:relative;height:30vh;width:40vw}.form-margin.svelte-1jlkcxq{margin:var(--dim-large-form-margin)}.flex-wrap.svelte-1jlkcxq{flex-wrap:wrap}table.disableFocusOutline.svelte-1ug7ecw.svelte-1ug7ecw:focus{outline:none}table.svelte-1ug7ecw.svelte-1ug7ecw{border-collapse:collapse;width:100%}table.selectable.svelte-1ug7ecw.svelte-1ug7ecw{user-select:none}tbody.svelte-1ug7ecw tr.svelte-1ug7ecw{background:var(--theme-bg-0)}tbody.svelte-1ug7ecw tr.selected.svelte-1ug7ecw{background:var(--theme-bg-selected)}tbody.svelte-1ug7ecw tr.clickable.svelte-1ug7ecw:hover{background:var(--theme-bg-hover)}thead.svelte-1ug7ecw td.svelte-1ug7ecw{border:1px solid var(--theme-border);background-color:var(--theme-bg-1);padding:5px}tbody.svelte-1ug7ecw td.svelte-1ug7ecw{border:1px solid var(--theme-border)}tbody.svelte-1ug7ecw td.svelte-1ug7ecw:not(.noCellPadding){padding:5px}td.isHighlighted.svelte-1ug7ecw.svelte-1ug7ecw{background-color:var(--theme-bg-1)}.title.svelte-lsle9{font-size:20px;text-align:center;margin:10px 0px}.column.svelte-lsle9{margin:10px;flex:1}.sqlwrap.svelte-lsle9{position:relative;z-index:0;height:100px;width:20vw;margin-left:var(--dim-large-form-margin);margin-bottom:var(--dim-large-form-margin)}.label.svelte-lsle9{margin-left:var(--dim-large-form-margin);margin-top:var(--dim-large-form-margin);margin-bottom:3px;color:var(--theme-font-3)}.buttons.svelte-lsle9{margin-left:var(--dim-large-form-margin)}.icon.svelte-170ou0a{cursor:pointer;color:var(--theme-font-link);margin-left:5px}.icon.svelte-170ou0a:hover{background-color:var(--theme-bg-2)}.container.svelte-abhawu{position:absolute;left:0;top:0;right:0;bottom:0;user-select:none;overflow:hidden}.table.svelte-abhawu{position:absolute;left:0;top:0;bottom:20px;overflow:scroll;border-collapse:collapse;outline:none}.header-cell.svelte-abhawu{border:1px solid var(--theme-border);text-align:left;padding:0;margin:0;background-color:var(--theme-bg-1);overflow:hidden}.filter-cell.svelte-abhawu{text-align:left;overflow:hidden;margin:0;padding:0}.focus-field.svelte-abhawu{position:absolute;left:-1000px;top:-1000px}.row-count-label.svelte-abhawu{position:absolute;background-color:var(--theme-bg-2);right:40px;bottom:20px}.main.svelte-1yczc9s{flex:1;display:flex;position:relative;overflow-y:scroll;background-color:var(--theme-bg-0)}table.svelte-1yczc9s{position:absolute;left:0;right:0;top:0;width:100%;border-spacing:0;border-collapse:collapse}td.header.svelte-1yczc9s{text-align:left;border-bottom:2px solid var(--theme-border);background-color:var(--theme-bg-1);padding:5px}td.svelte-1yczc9s:not(.header){border-top:1px solid var(--theme-border);padding:5px}tr.isActive.svelte-1yczc9s:hover{background:var(--theme-bg-2)}tr.isError.svelte-1yczc9s{color:var(--theme-icon-red)}.white-page.svelte-16npcmz{position:absolute;left:0;top:0;right:0;bottom:0;background-color:var(--theme-bg-0);overflow:auto;padding:10px}.header.svelte-16npcmz{display:flex;border-bottom:1px solid var(--theme-border);margin-bottom:20px;padding-bottom:20px}.title.svelte-16npcmz{font-size:20pt}.icon.svelte-16npcmz{width:80px;height:80px}div.svelte-skjeqm{padding:10px;overflow:auto;flex:1}div.svelte-skjeqm{padding:10px;overflow:auto;flex:1}.wrapper.svelte-1d8o0gh{flex:1;display:flex;flex-direction:column}.table-wrapper.svelte-1d8o0gh{overflow:auto;display:flex}.wrapper.svelte-lmwisg{overflow:auto;flex:1}.flexcol.svelte-lmwisg{flex:1;display:flex;flex-direction:column}.topbar.svelte-lmwisg{display:flex;margin:10px 0px;width:100%}.arrow.svelte-lmwisg{font-size:30px;color:var(--theme-icon-blue);align-self:center;position:relative}.deployButton.svelte-lmwisg{margin-left:20px;margin-right:20px}.tableWrapper.svelte-lmwisg{position:relative;width:100%;flex:1}.filters.svelte-lmwisg{display:flex;flex-wrap:wrap}div.svelte-skjeqm{padding:10px;overflow:auto;flex:1}.container.svelte-1awjfxf{display:flex;flex-direction:column;flex:1}.content.svelte-1awjfxf{flex:1;position:relative}.top-panel.svelte-1awjfxf{display:flex;background:var(--theme-bg-2)}.type.svelte-1awjfxf{font-weight:bold;margin-right:10px;align-self:center}.key-name.svelte-1awjfxf{flex-grow:1;display:flex}.key-name.svelte-1awjfxf input{flex-grow:1}.wrapper.svelte-yw1ll{position:absolute;left:0;top:0;right:0;bottom:0;background-color:var(--theme-bg-0);overflow:auto}.action-separator.svelte-yw1ll{margin:0 5px}.wrapper.svelte-1patgrk{flex:1;display:flex;flex-direction:column;overflow-y:auto}.buttons.svelte-1patgrk{flex-shrink:0;margin:var(--dim-large-form-margin)}.test-result.svelte-1patgrk{margin-left:10px;align-self:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.error-result.svelte-1patgrk{white-space:normal}.wrapper.svelte-1p2rqwm{overflow-y:auto;background-color:var(--theme-bg-0);flex:1;display:flex;flex-direction:column}.content.svelte-nk47x3{flex:1;display:flex;flex-direction:column;overflow-y:auto;overflow-x:hidden}.selectContainer.svelte-17l1npl.svelte-17l1npl{--internalPadding:0 16px;border:var(--border, 1px solid #d8dbdf);border-radius:var(--borderRadius, 3px);box-sizing:border-box;height:var(--height, 42px);position:relative;display:flex;align-items:center;padding:var(--padding, var(--internalPadding));background:var(--background, #fff);margin:var(--margin, 0)}.selectContainer.svelte-17l1npl input.svelte-17l1npl{cursor:default;border:none;color:var(--inputColor, #3f4f5f);height:var(--height, 42px);line-height:var(--height, 42px);padding:var(--inputPadding, var(--padding, var(--internalPadding)));width:100%;background:transparent;font-size:var(--inputFontSize, 14px);letter-spacing:var(--inputLetterSpacing, -0.08px);position:absolute;left:var(--inputLeft, 0);margin:var(--inputMargin, 0)}.selectContainer.svelte-17l1npl input.svelte-17l1npl::placeholder{color:var(--placeholderColor, #78848f);opacity:var(--placeholderOpacity, 1)}.selectContainer.svelte-17l1npl input.svelte-17l1npl:focus{outline:none}.selectContainer.svelte-17l1npl.svelte-17l1npl:hover{border-color:var(--borderHoverColor, #b2b8bf)}.selectContainer.focused.svelte-17l1npl.svelte-17l1npl{border-color:var(--borderFocusColor, #006fe8)}.selectContainer.disabled.svelte-17l1npl.svelte-17l1npl{background:var(--disabledBackground, #ebedef);border-color:var(--disabledBorderColor, #ebedef);color:var(--disabledColor, #c1c6cc)}.selectContainer.disabled.svelte-17l1npl input.svelte-17l1npl::placeholder{color:var(--disabledPlaceholderColor, #c1c6cc);opacity:var(--disabledPlaceholderOpacity, 1)}.selectedItem.svelte-17l1npl.svelte-17l1npl{line-height:var(--height, 42px);height:var(--height, 42px);overflow-x:hidden;padding:var(--selectedItemPadding, 0 20px 0 0)}.selectedItem.svelte-17l1npl.svelte-17l1npl:focus{outline:none}.clearSelect.svelte-17l1npl.svelte-17l1npl{position:absolute;right:var(--clearSelectRight, 10px);top:var(--clearSelectTop, 11px);bottom:var(--clearSelectBottom, 11px);width:var(--clearSelectWidth, 20px);color:var(--clearSelectColor, #c5cacf);flex:none !important}.clearSelect.svelte-17l1npl.svelte-17l1npl:hover{color:var(--clearSelectHoverColor, #2c3e50)}.selectContainer.focused.svelte-17l1npl .clearSelect.svelte-17l1npl{color:var(--clearSelectFocusColor, #3f4f5f)}.indicator.svelte-17l1npl.svelte-17l1npl{position:absolute;right:var(--indicatorRight, 10px);top:var(--indicatorTop, 11px);width:var(--indicatorWidth, 20px);height:var(--indicatorHeight, 20px);color:var(--indicatorColor, #c5cacf)}.indicator.svelte-17l1npl svg.svelte-17l1npl{display:inline-block;fill:var(--indicatorFill, currentcolor);line-height:1;stroke:var(--indicatorStroke, currentcolor);stroke-width:0}.spinner.svelte-17l1npl.svelte-17l1npl{position:absolute;right:var(--spinnerRight, 10px);top:var(--spinnerLeft, 11px);width:var(--spinnerWidth, 20px);height:var(--spinnerHeight, 20px);color:var(--spinnerColor, #51ce6c);animation:svelte-17l1npl-rotate 0.75s linear infinite}.spinner_icon.svelte-17l1npl.svelte-17l1npl{display:block;height:100%;transform-origin:center center;width:100%;position:absolute;top:0;bottom:0;left:0;right:0;margin:auto;-webkit-transform:none}.spinner_path.svelte-17l1npl.svelte-17l1npl{stroke-dasharray:90;stroke-linecap:round}.multiSelect.svelte-17l1npl.svelte-17l1npl{display:flex;padding:var(--multiSelectPadding, 0 35px 0 16px);height:auto;flex-wrap:wrap;align-items:stretch}.multiSelect.svelte-17l1npl>.svelte-17l1npl{flex:1 1 50px}.selectContainer.multiSelect.svelte-17l1npl input.svelte-17l1npl{padding:var(--multiSelectInputPadding, 0);position:relative;margin:var(--multiSelectInputMargin, 0)}.hasError.svelte-17l1npl.svelte-17l1npl{border:var(--errorBorder, 1px solid #ff2d55);background:var(--errorBackground, #fff)}.a11yText.svelte-17l1npl.svelte-17l1npl{z-index:9999;border:0px;clip:rect(1px, 1px, 1px, 1px);height:1px;width:1px;position:absolute;overflow:hidden;padding:0px;white-space:nowrap}@keyframes svelte-17l1npl-rotate{100%{transform:rotate(360deg)}}.br.svelte-hcq8xe{background:var(--theme-bg-2);height:1px;margin:5px 10px}.info.svelte-xmmjcw{margin-left:30px;color:var(--theme-font-3)}.wrapper.svelte-fyr7t5{padding:5px}.wrapper.svelte-fyr7t5:hover{background-color:var(--theme-bg-hover)}.info.svelte-fyr7t5{margin-left:30px;margin-top:5px;color:var(--theme-font-3)}.sql.svelte-fyr7t5{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.container.svelte-1vl91lb{display:flex;align-content:stretch;height:38px}.item.svelte-1vl91lb{flex-grow:1;margin:3px;border:1px solid var(--theme-border);border-radius:4px;font-size:12pt;display:flex;justify-content:space-around;align-items:center}.item.svelte-1vl91lb:hover:not(.disabled){border:1px solid var(--theme-font-2)}.item.selected.svelte-1vl91lb{border:2px solid var(--theme-font-1);margin:2px}.container.svelte-aetkv7{display:flex;flex:1;flex-direction:column}.wrapper.svelte-13i2vsu{overflow:auto}.outer.svelte-qjn8rh{flex:1;position:relative}.inner.svelte-qjn8rh{overflow:scroll;position:absolute;left:0;top:0;right:0;bottom:0}.wrapper.svelte-y6l14f{margin:var(--dim-large-form-margin)}.wrapper.svelte-5j61hy{padding:10px;background:var(--theme-bg-2)}.main.svelte-5j61hy{margin:var(--dim-large-form-margin)}.wrapper.svelte-1xz9rwb{margin:var(--dim-large-form-margin)}.header.svelte-13yk742{display:flex;flex-wrap:nowrap}.order-index.svelte-13yk742{font-size:10pt;margin-left:-3px;margin-right:2px;top:-1px;position:relative}.label.svelte-13yk742{flex:1;min-width:10px;padding:2px;margin:auto;white-space:nowrap}.icon.svelte-13yk742{margin-left:3px;align-self:center;font-size:18px}.grouping.svelte-13yk742{color:var(--theme-font-alt);white-space:nowrap}.data-type.svelte-13yk742{color:var(--theme-font-3)}.main.svelte-146rrm{overflow-x:scroll;height:16px;position:absolute;bottom:0;right:0;left:0}tr.svelte-1fsh2nj{background-color:var(--theme-bg-0)}tr.svelte-1fsh2nj:nth-child(6n + 3){background-color:var(--theme-bg-1)}tr.svelte-1fsh2nj:nth-child(6n + 6){background-color:var(--theme-bg-alt)}input.svelte-1tfc4w5{flex:1;min-width:10px;width:1px}input.isError.svelte-1tfc4w5{background-color:var(--theme-bg-red)}input.isOk.svelte-1tfc4w5{background-color:var(--theme-bg-green)}.main.svelte-17x38nz{overflow-y:scroll;width:20px;position:absolute;right:0px;width:20px;bottom:16px;top:0}div.svelte-1vtbbds{color:var(--theme-font-3);text-align:center}div.svelte-1vtbbds:hover{color:var(--theme-font-hover);border:1px solid var(--theme-font-1)}.sql.svelte-115tce0{position:relative;height:25vh;width:40vw}.editor.svelte-jgnle7{position:relative;height:30vh;width:40vw}.editor.svelte-1vqhgea{position:relative;height:30vh;width:40vw}.footer.svelte-1vqhgea{display:flex;justify-content:space-between}label.svelte-1oyc27i{border:1px solid var(--theme-bg-button-inv-2);padding:4px;margin:2px;width:100px;background-color:var(--theme-bg-button-inv);color:var(--theme-font-inv-1);border-radius:2px;position:relative;top:3px}label.svelte-1oyc27i:hover:not(.disabled){background-color:var(--theme-bg-button-inv-2)}label.svelte-1oyc27i:active:not(.disabled){background-color:var(--theme-bg-button-inv-3)}label.disabled.svelte-1oyc27i{background-color:var(--theme-bg-button-inv-3);color:var(--theme-font-inv-3)}.reference-container.svelte-1tqfmha{position:absolute;display:flex;flex-direction:column;top:0;left:0;right:0;bottom:0}.detail.svelte-1tqfmha{position:relative;flex:1}.wrapper.svelte-8bgi65{flex:1;display:flex;flex-direction:column}.content.svelte-8bgi65{border-bottom:1px solid var(--theme-border);display:flex;flex:1;position:relative}.toolstrip.svelte-8bgi65{display:flex;flex-wrap:wrap;background:var(--theme-bg-1)}.button.svelte-1ftx9ax{padding-left:5px;padding-right:5px;color:var(--theme-font-1);border:0;align-self:stretch;display:flex;user-select:none;margin:2px 0px}.button.disabled.svelte-1ftx9ax{color:var(--theme-font-3)}.inner.svelte-1ftx9ax:hover:not(.disabled){background:var(--theme-bg-3)}.inner.svelte-1ftx9ax:active:hover:not(.disabled){background:var(--theme-bg-4)}.icon.svelte-1ftx9ax{margin-right:5px;color:var(--theme-font-link)}.icon.disabled.svelte-1ftx9ax{color:var(--theme-font-3)}.inner.svelte-1ftx9ax{white-space:nowrap;align-self:center;background:var(--theme-bg-2);padding:3px 8px;border-radius:4px;cursor:pointer}.container.svelte-1naqcyl{flex:1;display:flex;flex-direction:column}.sql.svelte-1g1l9kr{position:relative;height:80px;width:40vw}.left.svelte-xxvqmu{display:flex;flex:1;background-color:var(--theme-bg-0)}.toolbar.svelte-17xquyn{background:var(--theme-bg-1);display:flex;border-bottom:1px solid var(--theme-border);border-top:2px solid var(--theme-border);margin-bottom:3px}.json.svelte-17xquyn{overflow:auto;flex:1}.wrapper.svelte-17xquyn{display:flex;flex-direction:column;position:absolute;left:0;top:0;right:0;bottom:0}.editor.svelte-jgnle7{position:relative;height:30vh;width:40vw}.label.svelte-1bc2dkx{white-space:nowrap}.label.notNull.svelte-1bc2dkx{font-weight:bold}.extinfo.svelte-1bc2dkx{font-weight:normal;margin-left:5px;color:var(--theme-font-3)}.left.svelte-1r4fguo{background-color:var(--theme-bg-0);display:flex;flex:1}.wrapper.svelte-u8tqy3{position:absolute;left:0;top:0;right:0;bottom:0;background-color:var(--theme-bg-0);overflow:auto}.listContainer.svelte-1uyqfml{box-shadow:var(--listShadow, 0 2px 3px 0 rgba(44, 62, 80, 0.24));border-radius:var(--listBorderRadius, 4px);max-height:var(--listMaxHeight, 250px);overflow-y:auto;background:var(--listBackground, #fff);border:var(--listBorder, none);position:var(--listPosition, absolute);z-index:var(--listZIndex, 2);width:100%;left:var(--listLeft, 0);right:var(--listRight, 0)}.virtualList.svelte-1uyqfml{height:var(--virtualListHeight, 200px)}.listGroupTitle.svelte-1uyqfml{color:var(--groupTitleColor, #8f8f8f);cursor:default;font-size:var(--groupTitleFontSize, 12px);font-weight:var(--groupTitleFontWeight, 600);height:var(--height, 42px);line-height:var(--height, 42px);padding:var(--groupTitlePadding, 0 20px);text-overflow:ellipsis;overflow-x:hidden;white-space:nowrap;text-transform:var(--groupTitleTextTransform, uppercase)}.empty.svelte-1uyqfml{text-align:var(--listEmptyTextAlign, center);padding:var(--listEmptyPadding, 20px 0);color:var(--listEmptyColor, #78848f)}.selection.svelte-pu1q1n{text-overflow:ellipsis;overflow-x:hidden;white-space:nowrap}.item.svelte-3e0qet{cursor:default;height:var(--height, 42px);line-height:var(--height, 42px);padding:var(--itemPadding, 0 20px);color:var(--itemColor, inherit);text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.groupHeader.svelte-3e0qet{text-transform:var(--groupTitleTextTransform, uppercase)}.groupItem.svelte-3e0qet{padding-left:var(--groupItemPaddingLeft, 40px)}.item.svelte-3e0qet:active{background:var(--itemActiveBackground, #b9daff)}.item.active.svelte-3e0qet{background:var(--itemIsActiveBG, #007aff);color:var(--itemIsActiveColor, #fff)}.item.notSelectable.svelte-3e0qet{color:var(--itemIsNotSelectableColor, #999)}.item.first.svelte-3e0qet{border-radius:var(--itemFirstBorderRadius, 4px 4px 0 0)}.item.hover.svelte-3e0qet:not(.active){background:var(--itemHoverBG, #e7f2ff);color:var(--itemHoverColor, inherit)}svelte-virtual-list-viewport.svelte-g2cagw{position:relative;overflow-y:auto;-webkit-overflow-scrolling:touch;display:block}svelte-virtual-list-contents.svelte-g2cagw,svelte-virtual-list-row.svelte-g2cagw{display:block}svelte-virtual-list-row.svelte-g2cagw{overflow:hidden}.multiSelectItem.svelte-liu9pa.svelte-liu9pa{background:var(--multiItemBG, #ebedef);margin:var(--multiItemMargin, 5px 5px 0 0);border-radius:var(--multiItemBorderRadius, 16px);height:var(--multiItemHeight, 32px);line-height:var(--multiItemHeight, 32px);display:flex;cursor:default;padding:var(--multiItemPadding, 0 10px 0 15px);max-width:100%}.multiSelectItem_label.svelte-liu9pa.svelte-liu9pa{margin:var(--multiLabelMargin, 0 5px 0 0);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.multiSelectItem.svelte-liu9pa.svelte-liu9pa:hover,.multiSelectItem.active.svelte-liu9pa.svelte-liu9pa{background-color:var(--multiItemActiveBG, #006fff);color:var(--multiItemActiveColor, #fff)}.multiSelectItem.disabled.svelte-liu9pa.svelte-liu9pa:hover{background:var(--multiItemDisabledHoverBg, #ebedef);color:var(--multiItemDisabledHoverColor, #c1c6cc)}.multiSelectItem_clear.svelte-liu9pa.svelte-liu9pa{border-radius:var(--multiClearRadius, 50%);background:var(--multiClearBG, #52616f);min-width:var(--multiClearWidth, 16px);max-width:var(--multiClearWidth, 16px);height:var(--multiClearHeight, 16px);position:relative;top:var(--multiClearTop, 8px);text-align:var(--multiClearTextAlign, center);padding:var(--multiClearPadding, 1px)}.multiSelectItem_clear.svelte-liu9pa.svelte-liu9pa:hover,.active.svelte-liu9pa .multiSelectItem_clear.svelte-liu9pa{background:var(--multiClearHoverBG, #fff)}.multiSelectItem_clear.svelte-liu9pa:hover svg.svelte-liu9pa,.active.svelte-liu9pa .multiSelectItem_clear svg.svelte-liu9pa{fill:var(--multiClearHoverFill, #006fff)}.multiSelectItem_clear.svelte-liu9pa svg.svelte-liu9pa{fill:var(--multiClearFill, #ebedef);vertical-align:top}.row.svelte-1h6n7am{margin:var(--dim-large-form-margin)}.root.svelte-ym7rtz{position:absolute;left:0;top:0;right:0;bottom:0;overflow-y:scroll;background:white;color:#000000}.wrapper.svelte-7kr1du.svelte-7kr1du{position:absolute;left:0;top:0;bottom:0;right:0}table.svelte-7kr1du.svelte-7kr1du{width:100%;flex:1}table.svelte-7kr1du thead.svelte-7kr1du,table.svelte-7kr1du tbody tr.svelte-7kr1du{display:table;width:100%;table-layout:fixed}table.svelte-7kr1du thead.svelte-7kr1du{width:calc(100% - 0.8em)}table.svelte-7kr1du tbody tr td.svelte-7kr1du{overflow:hidden}table.singleLineRow.svelte-7kr1du tbody tr td.svelte-7kr1du{white-space:nowrap}table.svelte-7kr1du tbody.svelte-7kr1du{display:block;overflow-y:scroll;overflow-x:hidden;table-layout:fixed;max-height:calc(100% - 20px)}table.disableFocusOutline.svelte-7kr1du.svelte-7kr1du:focus{outline:none}table.svelte-7kr1du.svelte-7kr1du{border-collapse:collapse;width:100%}table.selectable.svelte-7kr1du.svelte-7kr1du{user-select:none}tbody.svelte-7kr1du tr.svelte-7kr1du{background:var(--theme-bg-0)}tbody.svelte-7kr1du tr.selected.svelte-7kr1du{background:var(--theme-bg-selected)}tbody.svelte-7kr1du tr.clickable.svelte-7kr1du:hover{background:var(--theme-bg-hover)}thead.svelte-7kr1du td.svelte-7kr1du{border:1px solid var(--theme-border);background-color:var(--theme-bg-1);padding:5px}tbody.svelte-7kr1du td.svelte-7kr1du{border:1px solid var(--theme-border);padding:5px}td.isHighlighted.svelte-7kr1du.svelte-7kr1du{background-color:var(--theme-bg-1)}tr.isAdded.svelte-7kr1du.svelte-7kr1du{background:var(--theme-bg-green)}tr.isChanged.svelte-7kr1du.svelte-7kr1du{background:var(--theme-bg-orange)}tr.isDeleted.svelte-7kr1du.svelte-7kr1du{background:var(--theme-bg-red)}.switch.svelte-1muj49d{margin-left:5px}.container.svelte-tt47mf{display:flex;height:30vh}.wrapper.svelte-1um34k6{margin-bottom:20px}.header.svelte-1um34k6{background-color:var(--theme-bg-1);padding:5px}.title.svelte-1um34k6{font-weight:bold;margin-left:5px}.body.svelte-1um34k6{margin:20px}.row.svelte-10d5vjg{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1toqt3y{margin:var(--dim-large-form-margin);display:flex}.radio.svelte-1toqt3y{margin-left:var(--dim-large-form-margin);display:flex}.radio.svelte-1toqt3y label{margin-right:10px}.wrapper.svelte-1um34k6{margin-bottom:20px}.header.svelte-1um34k6{background-color:var(--theme-bg-1);padding:5px}.title.svelte-1um34k6{font-weight:bold;margin-left:5px}.body.svelte-1um34k6{margin:20px}td.svelte-xbqy26{border:1px solid var(--theme-border);text-align:left;padding:2px;background-color:var(--theme-bg-1);overflow:hidden;position:relative}.wrapper.svelte-ch62af{overflow:auto;flex:1}.props.svelte-1hio2dm{flex:1;display:flex;flex-direction:column}.left.svelte-cmv30q{display:flex;flex:1;background-color:var(--theme-bg-0)}.temp-root.svelte-cmv30q{border:1px solid var(--theme-border);background-color:var(--theme-bg-1);display:flex;justify-content:space-between;align-items:center;padding-left:2px}/* required styles */

.leaflet-pane,
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-marker-shadow,
.leaflet-tile-container,
.leaflet-pane > svg,
.leaflet-pane > canvas,
.leaflet-zoom-box,
.leaflet-image-layer,
.leaflet-layer {
	position: absolute;
	left: 0;
	top: 0;
	}
.leaflet-container {
	overflow: hidden;
	}
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-marker-shadow {
	-webkit-user-select: none;
	   -moz-user-select: none;
	        user-select: none;
	  -webkit-user-drag: none;
	}
/* Prevents IE11 from highlighting tiles in blue */
.leaflet-tile::selection {
	background: transparent;
}
/* Safari renders non-retina tile on retina better with this, but Chrome is worse */
.leaflet-safari .leaflet-tile {
	image-rendering: -webkit-optimize-contrast;
	}
/* hack that prevents hw layers "stretching" when loading new tiles */
.leaflet-safari .leaflet-tile-container {
	width: 1600px;
	height: 1600px;
	-webkit-transform-origin: 0 0;
	}
.leaflet-marker-icon,
.leaflet-marker-shadow {
	display: block;
	}
/* .leaflet-container svg: reset svg max-width decleration shipped in Joomla! (joomla.org) 3.x */
/* .leaflet-container img: map is broken in FF if you have max-width: 100% on tiles */
.leaflet-container .leaflet-overlay-pane svg {
	max-width: none !important;
	max-height: none !important;
	}
.leaflet-container .leaflet-marker-pane img,
.leaflet-container .leaflet-shadow-pane img,
.leaflet-container .leaflet-tile-pane img,
.leaflet-container img.leaflet-image-layer,
.leaflet-container .leaflet-tile {
	max-width: none !important;
	max-height: none !important;
	width: auto;
	padding: 0;
	}

.leaflet-container img.leaflet-tile {
	/* See: https://bugs.chromium.org/p/chromium/issues/detail?id=600120 */
	mix-blend-mode: plus-lighter;
}

.leaflet-container.leaflet-touch-zoom {
	-ms-touch-action: pan-x pan-y;
	touch-action: pan-x pan-y;
	}
.leaflet-container.leaflet-touch-drag {
	-ms-touch-action: pinch-zoom;
	/* Fallback for FF which doesn't support pinch-zoom */
	touch-action: none;
	touch-action: pinch-zoom;
}
.leaflet-container.leaflet-touch-drag.leaflet-touch-zoom {
	-ms-touch-action: none;
	touch-action: none;
}
.leaflet-container {
	-webkit-tap-highlight-color: transparent;
}
.leaflet-container a {
	-webkit-tap-highlight-color: rgba(51, 181, 229, 0.4);
}
.leaflet-tile {
	filter: inherit;
	visibility: hidden;
	}
.leaflet-tile-loaded {
	visibility: inherit;
	}
.leaflet-zoom-box {
	width: 0;
	height: 0;
	-moz-box-sizing: border-box;
	     box-sizing: border-box;
	z-index: 800;
	}
/* workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=888319 */
.leaflet-overlay-pane svg {
	-moz-user-select: none;
	}

.leaflet-pane         { z-index: 400; }

.leaflet-tile-pane    { z-index: 200; }
.leaflet-overlay-pane { z-index: 400; }
.leaflet-shadow-pane  { z-index: 500; }
.leaflet-marker-pane  { z-index: 600; }
.leaflet-tooltip-pane   { z-index: 650; }
.leaflet-popup-pane   { z-index: 700; }

.leaflet-map-pane canvas { z-index: 100; }
.leaflet-map-pane svg    { z-index: 200; }

.leaflet-vml-shape {
	width: 1px;
	height: 1px;
	}
.lvml {
	behavior: url(#default#VML);
	display: inline-block;
	position: absolute;
	}


/* control positioning */

.leaflet-control {
	position: relative;
	z-index: 800;
	pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
	pointer-events: auto;
	}
.leaflet-top,
.leaflet-bottom {
	position: absolute;
	z-index: 1000;
	pointer-events: none;
	}
.leaflet-top {
	top: 0;
	}
.leaflet-right {
	right: 0;
	}
.leaflet-bottom {
	bottom: 0;
	}
.leaflet-left {
	left: 0;
	}
.leaflet-control {
	float: left;
	clear: both;
	}
.leaflet-right .leaflet-control {
	float: right;
	}
.leaflet-top .leaflet-control {
	margin-top: 10px;
	}
.leaflet-bottom .leaflet-control {
	margin-bottom: 10px;
	}
.leaflet-left .leaflet-control {
	margin-left: 10px;
	}
.leaflet-right .leaflet-control {
	margin-right: 10px;
	}


/* zoom and fade animations */

.leaflet-fade-anim .leaflet-popup {
	opacity: 0;
	-webkit-transition: opacity 0.2s linear;
	   -moz-transition: opacity 0.2s linear;
	        transition: opacity 0.2s linear;
	}
.leaflet-fade-anim .leaflet-map-pane .leaflet-popup {
	opacity: 1;
	}
.leaflet-zoom-animated {
	-webkit-transform-origin: 0 0;
	    -ms-transform-origin: 0 0;
	        transform-origin: 0 0;
	}
svg.leaflet-zoom-animated {
	will-change: transform;
}

.leaflet-zoom-anim .leaflet-zoom-animated {
	-webkit-transition: -webkit-transform 0.25s cubic-bezier(0,0,0.25,1);
	   -moz-transition:    -moz-transform 0.25s cubic-bezier(0,0,0.25,1);
	        transition:         transform 0.25s cubic-bezier(0,0,0.25,1);
	}
.leaflet-zoom-anim .leaflet-tile,
.leaflet-pan-anim .leaflet-tile {
	-webkit-transition: none;
	   -moz-transition: none;
	        transition: none;
	}

.leaflet-zoom-anim .leaflet-zoom-hide {
	visibility: hidden;
	}


/* cursors */

.leaflet-interactive {
	cursor: pointer;
	}
.leaflet-grab {
	cursor: -webkit-grab;
	cursor:    -moz-grab;
	cursor:         grab;
	}
.leaflet-crosshair,
.leaflet-crosshair .leaflet-interactive {
	cursor: crosshair;
	}
.leaflet-popup-pane,
.leaflet-control {
	cursor: auto;
	}
.leaflet-dragging .leaflet-grab,
.leaflet-dragging .leaflet-grab .leaflet-interactive,
.leaflet-dragging .leaflet-marker-draggable {
	cursor: move;
	cursor: -webkit-grabbing;
	cursor:    -moz-grabbing;
	cursor:         grabbing;
	}

/* marker & overlays interactivity */
.leaflet-marker-icon,
.leaflet-marker-shadow,
.leaflet-image-layer,
.leaflet-pane > svg path,
.leaflet-tile-container {
	pointer-events: none;
	}

.leaflet-marker-icon.leaflet-interactive,
.leaflet-image-layer.leaflet-interactive,
.leaflet-pane > svg path.leaflet-interactive,
svg.leaflet-image-layer.leaflet-interactive path {
	pointer-events: visiblePainted; /* IE 9-10 doesn't have auto */
	pointer-events: auto;
	}

/* visual tweaks */

.leaflet-container {
	background: #ddd;
	outline-offset: 1px;
	}
.leaflet-container a {
	color: #0078A8;
	}
.leaflet-zoom-box {
	border: 2px dotted #38f;
	background: rgba(255,255,255,0.5);
	}


/* general typography */
.leaflet-container {
	font-family: "Helvetica Neue", Arial, Helvetica, sans-serif;
	font-size: 12px;
	font-size: 0.75rem;
	line-height: 1.5;
	}


/* general toolbar styles */

.leaflet-bar {
	box-shadow: 0 1px 5px rgba(0,0,0,0.65);
	border-radius: 4px;
	}
.leaflet-bar a {
	background-color: #fff;
	border-bottom: 1px solid #ccc;
	width: 26px;
	height: 26px;
	line-height: 26px;
	display: block;
	text-align: center;
	text-decoration: none;
	color: black;
	}
.leaflet-bar a,
.leaflet-control-layers-toggle {
	background-position: 50% 50%;
	background-repeat: no-repeat;
	display: block;
	}
.leaflet-bar a:hover,
.leaflet-bar a:focus {
	background-color: #f4f4f4;
	}
.leaflet-bar a:first-child {
	border-top-left-radius: 4px;
	border-top-right-radius: 4px;
	}
.leaflet-bar a:last-child {
	border-bottom-left-radius: 4px;
	border-bottom-right-radius: 4px;
	border-bottom: none;
	}
.leaflet-bar a.leaflet-disabled {
	cursor: default;
	background-color: #f4f4f4;
	color: #bbb;
	}

.leaflet-touch .leaflet-bar a {
	width: 30px;
	height: 30px;
	line-height: 30px;
	}
.leaflet-touch .leaflet-bar a:first-child {
	border-top-left-radius: 2px;
	border-top-right-radius: 2px;
	}
.leaflet-touch .leaflet-bar a:last-child {
	border-bottom-left-radius: 2px;
	border-bottom-right-radius: 2px;
	}

/* zoom control */

.leaflet-control-zoom-in,
.leaflet-control-zoom-out {
	font: bold 18px 'Lucida Console', Monaco, monospace;
	text-indent: 1px;
	}

.leaflet-touch .leaflet-control-zoom-in, .leaflet-touch .leaflet-control-zoom-out  {
	font-size: 22px;
	}


/* layers control */

.leaflet-control-layers {
	box-shadow: 0 1px 5px rgba(0,0,0,0.4);
	background: #fff;
	border-radius: 5px;
	}
.leaflet-control-layers-toggle {
	background-image: url(images/layers.png);
	width: 36px;
	height: 36px;
	}
.leaflet-retina .leaflet-control-layers-toggle {
	background-image: url(images/layers-2x.png);
	background-size: 26px 26px;
	}
.leaflet-touch .leaflet-control-layers-toggle {
	width: 44px;
	height: 44px;
	}
.leaflet-control-layers .leaflet-control-layers-list,
.leaflet-control-layers-expanded .leaflet-control-layers-toggle {
	display: none;
	}
.leaflet-control-layers-expanded .leaflet-control-layers-list {
	display: block;
	position: relative;
	}
.leaflet-control-layers-expanded {
	padding: 6px 10px 6px 6px;
	color: #333;
	background: #fff;
	}
.leaflet-control-layers-scrollbar {
	overflow-y: scroll;
	overflow-x: hidden;
	padding-right: 5px;
	}
.leaflet-control-layers-selector {
	margin-top: 2px;
	position: relative;
	top: 1px;
	}
.leaflet-control-layers label {
	display: block;
	font-size: 13px;
	font-size: 1.08333em;
	}
.leaflet-control-layers-separator {
	height: 0;
	border-top: 1px solid #ddd;
	margin: 5px -10px 5px -6px;
	}

/* Default icon URLs */
.leaflet-default-icon-path { /* used only in path-guessing heuristic, see L.Icon.Default */
	background-image: url(images/marker-icon.png);
	}


/* attribution and scale controls */

.leaflet-container .leaflet-control-attribution {
	background: #fff;
	background: rgba(255, 255, 255, 0.8);
	margin: 0;
	}
.leaflet-control-attribution,
.leaflet-control-scale-line {
	padding: 0 5px;
	color: #333;
	line-height: 1.4;
	}
.leaflet-control-attribution a {
	text-decoration: none;
	}
.leaflet-control-attribution a:hover,
.leaflet-control-attribution a:focus {
	text-decoration: underline;
	}
.leaflet-attribution-flag {
	display: inline !important;
	vertical-align: baseline !important;
	width: 1em;
	height: 0.6669em;
	}
.leaflet-left .leaflet-control-scale {
	margin-left: 5px;
	}
.leaflet-bottom .leaflet-control-scale {
	margin-bottom: 5px;
	}
.leaflet-control-scale-line {
	border: 2px solid #777;
	border-top: none;
	line-height: 1.1;
	padding: 2px 5px 1px;
	white-space: nowrap;
	-moz-box-sizing: border-box;
	     box-sizing: border-box;
	background: rgba(255, 255, 255, 0.8);
	text-shadow: 1px 1px #fff;
	}
.leaflet-control-scale-line:not(:first-child) {
	border-top: 2px solid #777;
	border-bottom: none;
	margin-top: -2px;
	}
.leaflet-control-scale-line:not(:first-child):not(:last-child) {
	border-bottom: 2px solid #777;
	}

.leaflet-touch .leaflet-control-attribution,
.leaflet-touch .leaflet-control-layers,
.leaflet-touch .leaflet-bar {
	box-shadow: none;
	}
.leaflet-touch .leaflet-control-layers,
.leaflet-touch .leaflet-bar {
	border: 2px solid rgba(0,0,0,0.2);
	background-clip: padding-box;
	}


/* popup */

.leaflet-popup {
	position: absolute;
	text-align: center;
	margin-bottom: 20px;
	}
.leaflet-popup-content-wrapper {
	padding: 1px;
	text-align: left;
	border-radius: 12px;
	}
.leaflet-popup-content {
	margin: 13px 24px 13px 20px;
	line-height: 1.3;
	font-size: 13px;
	font-size: 1.08333em;
	min-height: 1px;
	}
.leaflet-popup-content p {
	margin: 17px 0;
	margin: 1.3em 0;
	}
.leaflet-popup-tip-container {
	width: 40px;
	height: 20px;
	position: absolute;
	left: 50%;
	margin-top: -1px;
	margin-left: -20px;
	overflow: hidden;
	pointer-events: none;
	}
.leaflet-popup-tip {
	width: 17px;
	height: 17px;
	padding: 1px;

	margin: -10px auto 0;
	pointer-events: auto;

	-webkit-transform: rotate(45deg);
	   -moz-transform: rotate(45deg);
	    -ms-transform: rotate(45deg);
	        transform: rotate(45deg);
	}
.leaflet-popup-content-wrapper,
.leaflet-popup-tip {
	background: white;
	color: #333;
	box-shadow: 0 3px 14px rgba(0,0,0,0.4);
	}
.leaflet-container a.leaflet-popup-close-button {
	position: absolute;
	top: 0;
	right: 0;
	border: none;
	text-align: center;
	width: 24px;
	height: 24px;
	font: 16px/24px Tahoma, Verdana, sans-serif;
	color: #757575;
	text-decoration: none;
	background: transparent;
	}
.leaflet-container a.leaflet-popup-close-button:hover,
.leaflet-container a.leaflet-popup-close-button:focus {
	color: #585858;
	}
.leaflet-popup-scrolled {
	overflow: auto;
	}

.leaflet-oldie .leaflet-popup-content-wrapper {
	-ms-zoom: 1;
	}
.leaflet-oldie .leaflet-popup-tip {
	width: 24px;
	margin: 0 auto;

	-ms-filter: "progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678)";
	filter: progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678);
	}

.leaflet-oldie .leaflet-control-zoom,
.leaflet-oldie .leaflet-control-layers,
.leaflet-oldie .leaflet-popup-content-wrapper,
.leaflet-oldie .leaflet-popup-tip {
	border: 1px solid #999;
	}


/* div icon */

.leaflet-div-icon {
	background: #fff;
	border: 1px solid #666;
	}


/* Tooltip */
/* Base styles for the element that has a tooltip */
.leaflet-tooltip {
	position: absolute;
	padding: 6px;
	background-color: #fff;
	border: 1px solid #fff;
	border-radius: 3px;
	color: #222;
	white-space: nowrap;
	-webkit-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
	pointer-events: none;
	box-shadow: 0 1px 3px rgba(0,0,0,0.4);
	}
.leaflet-tooltip.leaflet-interactive {
	cursor: pointer;
	pointer-events: auto;
	}
.leaflet-tooltip-top:before,
.leaflet-tooltip-bottom:before,
.leaflet-tooltip-left:before,
.leaflet-tooltip-right:before {
	position: absolute;
	pointer-events: none;
	border: 6px solid transparent;
	background: transparent;
	content: "";
	}

/* Directions */

.leaflet-tooltip-bottom {
	margin-top: 6px;
}
.leaflet-tooltip-top {
	margin-top: -6px;
}
.leaflet-tooltip-bottom:before,
.leaflet-tooltip-top:before {
	left: 50%;
	margin-left: -6px;
	}
.leaflet-tooltip-top:before {
	bottom: 0;
	margin-bottom: -12px;
	border-top-color: #fff;
	}
.leaflet-tooltip-bottom:before {
	top: 0;
	margin-top: -12px;
	margin-left: -6px;
	border-bottom-color: #fff;
	}
.leaflet-tooltip-left {
	margin-left: -6px;
}
.leaflet-tooltip-right {
	margin-left: 6px;
}
.leaflet-tooltip-left:before,
.leaflet-tooltip-right:before {
	top: 50%;
	margin-top: -6px;
	}
.leaflet-tooltip-left:before {
	right: 0;
	margin-right: -12px;
	border-left-color: #fff;
	}
.leaflet-tooltip-right:before {
	left: 0;
	margin-left: -12px;
	border-right-color: #fff;
	}

/* Printing */

@media print {
	/* Prevent printers from removing background-images of controls. */
	.leaflet-control {
		-webkit-print-color-adjust: exact;
		print-color-adjust: exact;
		}
	}
.container.svelte-eg2ir1{display:flex;flex-direction:column;height:30vh}.wrapper.svelte-11a2g2s{margin:1px 3px 10px 5px;display:flex;align-items:center}.wrapper.svelte-11a2g2s:hover{background-color:var(--theme-bg-selected)}.icon.svelte-11a2g2s{width:50px;height:50px}.builtin.svelte-11a2g2s{color:var(--theme-font-3)}li.svelte-3bjyvl{user-select:text;word-wrap:break-word;word-break:break-all}.indent.svelte-3bjyvl{padding-left:var(--li-identation)}.String.svelte-3bjyvl{color:var(--string-color)}.Date.svelte-3bjyvl{color:var(--date-color)}.Number.svelte-3bjyvl{color:var(--number-color)}.Boolean.svelte-3bjyvl{color:var(--boolean-color)}.Null.svelte-3bjyvl{color:var(--null-color)}.Undefined.svelte-3bjyvl{color:var(--undefined-color)}.Function.svelte-3bjyvl{color:var(--function-color);font-style:italic}.Symbol.svelte-3bjyvl{color:var(--symbol-color)}li.svelte-1ca3gb2{user-select:text;word-wrap:break-word;word-break:break-all}.indent.svelte-1ca3gb2{padding-left:var(--li-identation)}.collapse.svelte-1ca3gb2{--li-display:inline;display:inline;font-style:italic}.row.svelte-1ecnyiy.svelte-1ecnyiy{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1ecnyiy .label.svelte-1ecnyiy{white-space:nowrap;align-self:center}.button.svelte-1ecnyiy.svelte-1ecnyiy{align-self:center;text-align:right}.tableWrapper.svelte-1ae830f{position:relative;max-height:300px;height:300px}td.svelte-1do4nz4{font-weight:normal;border:1px solid var(--theme-border);padding:2px;white-space:nowrap;position:relative;overflow:hidden}td.isFrameSelected.svelte-1do4nz4{outline:3px solid var(--theme-bg-selected);outline-offset:-3px}td.isAutofillSelected.svelte-1do4nz4{outline:3px solid var(--theme-bg-selected);outline-offset:-3px}td.isFocusedColumn.svelte-1do4nz4{background:var(--theme-bg-alt)}td.isModifiedRow.svelte-1do4nz4{background:var(--theme-bg-gold)}td.isModifiedCell.svelte-1do4nz4{background:var(--theme-bg-orange)}td.isInserted.svelte-1do4nz4{background:var(--theme-bg-green)}td.isDeleted.svelte-1do4nz4{background:var(--theme-bg-volcano)}td.isSelected.svelte-1do4nz4{background:var(--theme-bg-selected)}td.isDeleted.svelte-1do4nz4{background-image:url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAEElEQVQImWNgIAX8x4KJBAD+agT8INXz9wAAAABJRU5ErkJggg==');background-repeat:repeat-x;background-position:50% 50%}.hint.svelte-1do4nz4{color:var(--theme-font-3);margin-left:5px}.autoFillMarker.svelte-1do4nz4{width:8px;height:8px;background:var(--theme-bg-selected-point);position:absolute;right:0px;bottom:0px;overflow:visible;cursor:crosshair}td.editor.svelte-1ye29ic{position:relative}.row.svelte-10d5vjg{margin:var(--dim-large-form-margin);display:flex}.tableWrapper.svelte-1ae830f{position:relative;max-height:300px;height:300px}.list.svelte-1frbq1k{max-height:25vh;overflow:scroll;user-select:none}.label.svelte-1frbq1k{cursor:pointer}.container.svelte-1jjkvl8{display:flex;justify-content:space-between;align-items:center;background:var(--theme-bg-modalheader);height:var(--dim-toolbar-height);min-height:var(--dim-toolbar-height);overflow:hidden;border-top:1px solid var(--theme-border);border-bottom:1px solid var(--theme-border)}.header.svelte-1jjkvl8{font-weight:bold;margin-left:10px;display:flex}.main1.svelte-kvh071 .wrapper.svelte-kvh071{position:relative;display:flex;width:100%;height:100%}.main2.svelte-kvh071 .wrapper.svelte-kvh071{position:relative;display:flex;width:100%;height:calc(50% - 2px);border-bottom:2px solid var(--theme-border)}.main3.svelte-kvh071 .wrapper.svelte-kvh071{position:relative;display:flex;width:100%;height:40%;border-bottom:2px solid var(--theme-border)}.main.svelte-kvh071.svelte-kvh071{position:absolute;left:0;top:0;right:0;bottom:0}.main3.svelte-kvh071.svelte-kvh071{overflow-y:scroll}.focus-field.svelte-1mcb02n{position:absolute;left:-1000px;top:-1000px}.selectwrap.svelte-1mcb02n select{flex:1;padding:3px 0px;border:none}.selectwrap.svelte-1mcb02n{border-bottom:1px solid var(--theme-border)}.link.svelte-jntsgu{color:var(--theme-font-link);margin:5px;cursor:pointer;display:flex;flex-wrap:nowrap}.link.svelte-jntsgu:hover{text-decoration:underline}.wrapper.svelte-90nftc input{width:100px}.wrapper.svelte-90nftc{display:flex;align-items:center}.label.svelte-90nftc{margin-left:5px;margin-right:5px}.container.svelte-7rm6j6{position:absolute;display:flex;flex-direction:column;top:0;left:0;right:0;bottom:0}div.svelte-jy5e9j{flex:1 1;overflow-y:auto;overflow-x:auto}div.isFlex.svelte-jy5e9j{display:flex}.wrapper.svelte-3ovaru{flex:1;overflow:hidden}.row.svelte-10d5vjg{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1ecnyiy.svelte-1ecnyiy{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1ecnyiy .label.svelte-1ecnyiy{white-space:nowrap;align-self:center}.button.svelte-1ecnyiy.svelte-1ecnyiy{align-self:center;text-align:right}div.svelte-2qh9ne{position:absolute;right:0px;top:1px;color:var(--theme-font-3);background-color:var(--theme-bg-1);border:1px solid var(--theme-bg-1)}div.svelte-2qh9ne:hover{color:var(--theme-font-hover);border:var(--theme-border);top:1px;right:0px}svg.svelte-j16aco{position:absolute;left:0;top:0;right:0;bottom:0;width:100%;height:100%}polyline.svelte-j16aco{fill:none;stroke:var(--theme-bg-4);stroke-width:2}polygon.svelte-j16aco{fill:var(--theme-font-1)}.wrapper.svelte-1tqsb1.svelte-1tqsb1{flex:1;background-color:var(--theme-bg-1);overflow:scroll}.empty.svelte-1tqsb1.svelte-1tqsb1{margin:50px;font-size:20px;position:absolute}.canvas.svelte-1tqsb1.svelte-1tqsb1{position:relative}.panel.svelte-1tqsb1.svelte-1tqsb1{position:absolute;right:16px;top:0;display:flex}.searchbox.svelte-1tqsb1.svelte-1tqsb1{width:200px;display:flex;margin-left:1px}svg.drag-rect.svelte-1tqsb1.svelte-1tqsb1{visibility:hidden;pointer-events:none}.dbgate-screen svg.drag-rect.svelte-1tqsb1.svelte-1tqsb1{visibility:visible;position:absolute;left:0;top:0;right:0;bottom:0;width:100%;height:100%}.dbgate-screen svg.drag-rect.svelte-1tqsb1 polyline.svelte-1tqsb1{fill:none;stroke:var(--theme-bg-4);stroke-width:2}svg.svelte-1k22hy3{position:absolute;left:0;top:0;right:0;bottom:0;width:100%;height:100%}polyline.svelte-1k22hy3{fill:none;stroke:var(--theme-bg-4);stroke-width:2}.wrapper.svelte-1k22hy3{position:absolute;border:1px solid var(--theme-border);background-color:var(--theme-bg-1);z-index:900;border-radius:10px;width:32px;height:32px}.text.svelte-1k22hy3{position:relative;float:left;top:50%;left:50%;transform:translate(-50%, -50%);z-index:900;white-space:nowrap;background-color:var(--theme-bg-1)}.colname.svelte-ouq9eo{color:var(--theme-font-3)}.colvalue.svelte-ouq9eo{position:relative;flex:1;display:flex}.colnamewrap.svelte-ouq9eo{display:flex;margin:20px 5px 5px 5px;justify-content:space-between}.outer.svelte-ouq9eo{flex:1;position:relative}.inner.svelte-ouq9eo{overflow:scroll;position:absolute;left:0;top:0;right:0;bottom:0}.row.svelte-1ecnyiy.svelte-1ecnyiy{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1ecnyiy .label.svelte-1ecnyiy{white-space:nowrap;align-self:center}.button.svelte-1ecnyiy.svelte-1ecnyiy{align-self:center;text-align:right}.msg.svelte-xvsamk{background:var(--theme-bg-1);flex:1;padding:10px}.wrapper.svelte-msvx43.svelte-msvx43{overflow:scroll;flex:1}table.svelte-msvx43.svelte-msvx43{overflow:scroll;outline:none;border-collapse:separate;border-spacing:0}table.svelte-msvx43 thead.svelte-msvx43{position:sticky;top:0;z-index:100}thead.svelte-msvx43 tr:first-child th{border-top:1px solid var(--theme-border)}.loader.svelte-msvx43.svelte-msvx43{position:absolute;right:0;bottom:0}label.svelte-rwxv37{display:inline-block}.indent.svelte-rwxv37{padding-left:var(--li-identation)}.collapse.svelte-rwxv37{--li-display:inline;display:inline;font-style:italic}.comma.svelte-rwxv37{margin-left:-0.5em;margin-right:0.5em}label.svelte-rwxv37{position:relative}label.svelte-1vlbacg{display:inline-block;color:var(--label-color);padding:0}.spaced.svelte-1vlbacg{padding-right:var(--li-colon-space)}.container.svelte-1vyml86{display:inline-block;cursor:pointer;transform:translate(calc(0px - var(--li-identation)), -50%);position:absolute;top:50%;padding-right:100%}.arrow.svelte-1vyml86{transform-origin:25% 50%;position:relative;line-height:1.1em;font-size:0.75em;margin-left:0;transition:150ms;color:var(--arrow-sign);user-select:none;font-family:'Courier New', Courier, monospace}.expanded.svelte-1vyml86{transform:rotateZ(90deg) translateX(-3px)}.wrapper.svelte-y6l14f{margin:var(--dim-large-form-margin)}.null.svelte-7yy3rb{color:var(--theme-font-3);font-style:italic}.value.svelte-7yy3rb{color:var(--theme-icon-green)}input.svelte-voroxd{border:0 solid;outline:none;margin:0;padding:0 1px}input.showEditorButton.svelte-voroxd{margin-right:16px}.options.svelte-1csa2ek{position:absolute;z-index:10;top:100%;left:0;width:100%;list-style:none;margin:0;padding:0;background-color:var(--theme-bg-alt);max-height:150px;overflow:auto;box-shadow:0 1px 10px 1px var(--theme-bg-inv-3);;}.value.svelte-1csa2ek{position:absolute;top:0;left:0;z-index:20;min-height:17px;background-color:var(--theme-bg-0);height:100%;width:calc(100% - 4px);padding:0 2px;display:flex;align-items:center;overflow-x:hidden}.confirm.svelte-1csa2ek{position:absolute;top:0;right:0;z-index:30}.hidden.svelte-1csa2ek{display:none}label.svelte-1csa2ek{padding:2px 3px;border-bottom:1px solid var(--theme-border);display:block;min-height:16px}label.svelte-1csa2ek:hover{background-color:var(--theme-bg-hover)}.button.svelte-nuulrm{padding-left:5px;padding-right:5px;color:var(--theme-font-1);border:0;align-self:stretch;display:flex;user-select:none;margin:2px 0px}.button.disabled.svelte-nuulrm{color:var(--theme-font-3)}.main.svelte-nuulrm{background:var(--theme-bg-2);padding:3px 0px 3px 8px;border-radius:4px 0px 0px 4px}.main.svelte-nuulrm:hover:not(.disabled){background:var(--theme-bg-3)}.main.svelte-nuulrm:active:hover:not(.disabled){background:var(--theme-bg-4)}.split-icon.svelte-nuulrm:hover:not(.disabled){background:var(--theme-bg-3)}.split-icon.svelte-nuulrm:active:hover:not(.disabled){background:var(--theme-bg-4)}.split-icon.svelte-nuulrm{background:var(--theme-bg-2);padding:3px 8px 3px 0px;border-radius:0px 4px 4px 0px}.icon.svelte-nuulrm{margin-right:5px;color:var(--theme-font-link)}.icon.disabled.svelte-nuulrm{color:var(--theme-font-3)}.inner.svelte-nuulrm{white-space:nowrap;align-self:center;cursor:pointer;display:flex}.main.svelte-nuulrm{display:flex;padding-right:5px}.split-icon.svelte-nuulrm{padding-left:5px;color:var(--theme-font-link);border-left:1px solid var(--theme-bg-4)}.row.svelte-1jp8z8u{margin-left:5px;margin-right:5px;cursor:pointer;white-space:nowrap;display:flex;justify-content:space-between}.row.svelte-1jp8z8u:hover{background:var(--theme-bg-hover)}.row.isSelected.svelte-1jp8z8u{background:var(--theme-bg-selected)}.icon.svelte-1jp8z8u{position:relative}.icon.svelte-1jp8z8u:hover{background-color:var(--theme-bg-3)}table.svelte-dxjwf3{border-collapse:collapse;outline:none}.outer.svelte-dxjwf3{position:absolute;left:0;top:0;bottom:0;right:0}.wrapper.svelte-dxjwf3{position:absolute;left:0;top:0;bottom:0;right:0;display:flex;overflow-x:scroll;align-items:flex-start}tr.svelte-dxjwf3{background-color:var(--theme-bg-0)}tr.svelte-dxjwf3:nth-child(6n + 3){background-color:var(--theme-bg-1)}tr.svelte-dxjwf3:nth-child(6n + 6){background-color:var(--theme-bg-alt)}.header-cell.svelte-dxjwf3{border:1px solid var(--theme-border);text-align:left;padding:0;margin:0;background-color:var(--theme-bg-1);overflow:hidden}.header-cell.isSelected.svelte-dxjwf3{background:var(--theme-bg-selected)}.header-cell-inner.svelte-dxjwf3{display:flex}.focus-field.svelte-dxjwf3{position:absolute;left:-1000px;top:-1000px}.row-count-label.svelte-dxjwf3{position:absolute;background-color:var(--theme-bg-2);right:40px;bottom:20px}.columnFiltered.svelte-dxjwf3{background:var(--theme-bg-green)}.container.svelte-161tttp{display:flex;justify-content:space-between;align-items:stretch;background:var(--theme-bg-modalheader);height:var(--dim-toolbar-height);min-height:var(--dim-toolbar-height);overflow:hidden;border-top:1px solid var(--theme-border);border-bottom:1px solid var(--theme-border)}.header.svelte-161tttp{font-weight:bold;margin-left:10px;display:flex;align-items:center}.buttons.svelte-161tttp{display:flex;align-items:stretch}.wrapper.svelte-1elitvt{display:flex;overflow-y:auto}.section.svelte-1elitvt{margin:5px}.row.svelte-1ecnyiy.svelte-1ecnyiy{margin:var(--dim-large-form-margin);display:flex}.row.svelte-1ecnyiy .label.svelte-1ecnyiy{white-space:nowrap;align-self:center}.button.svelte-1ecnyiy.svelte-1ecnyiy{align-self:center;text-align:right}.wrapper.svelte-uqb2wg{border:1px solid var(--theme-border);padding:3px;color:var(--theme-font-2)}.wrapper.svelte-w5ultk{position:absolute;background-color:var(--theme-bg-0);border:1px solid var(--theme-border)}.selection-marker.svelte-w5ultk{display:none;position:absolute;width:6px;height:6px;background:var(--theme-font-1)}.selection-marker.lt.svelte-w5ultk{left:-3px;top:-3px}.selection-marker.rt.svelte-w5ultk{right:-3px;top:-3px}.selection-marker.lb.svelte-w5ultk{left:-3px;bottom:-3px}.selection-marker.rb.svelte-w5ultk{right:-3px;bottom:-3px}.dbgate-screen .selection-marker.svelte-w5ultk{display:block}.dbgate-screen .wrapper.svelte-w5ultk:not(.canSelectColumns){cursor:pointer}.header.svelte-w5ultk{font-weight:bold;text-align:center;padding:2px;border-bottom:1px solid var(--theme-border);display:flex;justify-content:space-between}.dbgate-screen .header.svelte-w5ultk{cursor:pointer}.header.isTable.svelte-w5ultk{background:var(--theme-bg-blue)}.header.isView.svelte-w5ultk{background:var(--theme-bg-magenta)}.header.isCollection.svelte-w5ultk{background:var(--theme-bg-red)}.header.isGrayed.svelte-w5ultk{background:var(--theme-bg-2)}.close.svelte-w5ultk{background:var(--theme-bg-1)}.close.svelte-w5ultk:hover{background:var(--theme-bg-2)}.close.svelte-w5ultk:active:hover{background:var(--theme-bg-3)}.columns.svelte-w5ultk{width:calc(100% - 10px);padding:5px}.columns.scroll.svelte-w5ultk{max-height:400px;overflow-y:auto}.row.svelte-n2q9l8{margin-left:5px;margin-right:5px;cursor:pointer;white-space:nowrap}.row.svelte-n2q9l8:hover{background:var(--theme-bg-hover)}.lds-spinner.svelte-bxata.svelte-bxata{color:official;display:inline-block;position:relative;width:80px;height:80px}.lds-spinner.svelte-bxata div.svelte-bxata{transform-origin:40px 40px;animation:svelte-bxata-lds-spinner 1.2s linear infinite}.lds-spinner.svelte-bxata div.svelte-bxata:after{content:' ';display:block;position:absolute;top:3px;left:37px;width:6px;height:18px;border-radius:20%;background:var(--theme-font-2)}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(1){transform:rotate(0deg);animation-delay:-1.1s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(2){transform:rotate(30deg);animation-delay:-1s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(3){transform:rotate(60deg);animation-delay:-0.9s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(4){transform:rotate(90deg);animation-delay:-0.8s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(5){transform:rotate(120deg);animation-delay:-0.7s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(6){transform:rotate(150deg);animation-delay:-0.6s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(7){transform:rotate(180deg);animation-delay:-0.5s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(8){transform:rotate(210deg);animation-delay:-0.4s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(9){transform:rotate(240deg);animation-delay:-0.3s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(10){transform:rotate(270deg);animation-delay:-0.2s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(11){transform:rotate(300deg);animation-delay:-0.1s}.lds-spinner.svelte-bxata div.svelte-bxata:nth-child(12){transform:rotate(330deg);animation-delay:0s}@keyframes svelte-bxata-lds-spinner{0%{opacity:1}100%{opacity:0}}.wrap.svelte-uz4mu9{display:flex}.label.svelte-uz4mu9{flex-wrap:nowrap}.label.svelte-uz4mu9{flex:1;min-width:10px;padding:2px;margin:auto;white-space:nowrap}.icon.svelte-uz4mu9{margin-left:3px;align-self:center;font-size:18px}th.svelte-uz4mu9{text-align:left;padding:2px;margin:0;background-color:var(--theme-bg-1);overflow:hidden;vertical-align:center;z-index:100;font-weight:normal;border-bottom:1px solid var(--theme-border);border-right:1px solid var(--theme-border)}th.tableHeader.svelte-uz4mu9{font-weight:bold}th.columnHeader.svelte-uz4mu9{position:relative}th.svelte-uz4mu9.highlight{border:3px solid var(--theme-icon-blue);padding:0px}td.svelte-1tkw7jt{font-weight:normal;background-color:var(--theme-bg-0);padding:2px;position:relative;overflow:hidden;vertical-align:top;border-bottom:1px solid var(--theme-border);border-right:1px solid var(--theme-border)}td.isEmpty.svelte-1tkw7jt{background-color:var(--theme-bg-1)}td.svelte-1tkw7jt.highlight{border:3px solid var(--theme-icon-blue);padding:0px}.null.svelte-1tkw7jt{color:var(--theme-font-3);font-style:italic}.dbgate-screen .line.canSelectColumns.svelte-1s00ucb:hover{background:var(--theme-bg-1)}.dbgate-screen .line.isDragSource.svelte-1s00ucb{background:var(--theme-bg-gold)}.dbgate-screen .line.isDragTarget.svelte-1s00ucb{background:var(--theme-bg-gold)}.line.svelte-1s00ucb{display:flex}.space.svelte-1s00ucb{flex-grow:1}.icon-button.svelte-1s00ucb{margin-left:4px;cursor:pointer}.icon-button.svelte-1s00ucb:hover{background:var(--theme-bg-2);color:var(--theme-font-hover)}.row.svelte-qzbyei{display:flex;margin:10px}.label.svelte-qzbyei{width:10vw;font-weight:bold}

        body {
          background: var(--theme-bg-1);
          color: var(--theme-font-1);
        }
      </style>

      <link rel="stylesheet" href='https://cdn.jsdelivr.net/npm/@mdi/font@6.5.95/css/materialdesignicons.css' />
  </head>
  
  <body class='theme-type-light theme-light'>
      <div class="canvas svelte-1tqsb1" style="width:3000px;height:3000px;
      
    "><svg class="svelte-j16aco"><polyline points="
      1189.796875,748.71875
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1132.5222050082934 238)"><polygon transform="rotate(83.6012870252033)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1189.796875,748.71875
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1279.8752344196737 555.3828125)"><polygon transform="rotate(114.98157771068793)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1189.796875,748.71875
      772.23046875,282.1953125
  " class="svelte-j16aco"></polyline><g transform="translate(831.5281849854517 348.4453125)"><polygon transform="rotate(48.16955270926766)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1310.7421875,489.1328125
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1169.712459161558 238)"><polygon transform="rotate(60.682553797625914)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      944.17578125,746
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1098.1592503570673 238)"><polygon transform="rotate(106.86295167138762)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      944.17578125,746
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1236.3046875 541.2940333416364)"><polygon transform="rotate(144.97959235756164)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      944.17578125,746
      772.23046875,282.1953125
  " class="svelte-j16aco"></polyline><g transform="translate(796.7911885101361 348.4453125)"><polygon transform="rotate(69.6588541200963)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1623.9375,310.3828125
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1188.765625 175.55143860003275)"><polygon transform="rotate(17.214798349990673)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1623.9375,310.3828125
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1385.1796875 446.6490887852653)"><polygon transform="rotate(330.2852951990451)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1623.9375,310.3828125
      772.23046875,282.1953125
  " class="svelte-j16aco"></polyline><g transform="translate(841.5703125 284.49013545436094)"><polygon transform="rotate(1.8955291761486137)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      772.23046875,282.1953125
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1057.71875 178.94691040268646)"><polygon transform="rotate(160.11719829675317)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      772.23046875,282.1953125
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1236.3046875 460.52821649973885)"><polygon transform="rotate(201.02060400426237)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1612.24609375,504.2265625
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1188.765625 202.01065710248832)"><polygon transform="rotate(35.513468644597936)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1612.24609375,504.2265625
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1385.1796875 492.85926841760056)"><polygon transform="rotate(2.865922430600193)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      733.73828125,617.5
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1057.71875 233.01098903854063)"><polygon transform="rotate(130.11836253746415)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      733.73828125,617.5
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1236.3046875 505.6930687062919)"><polygon transform="rotate(167.45755768442572)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      733.73828125,617.5
      772.23046875,282.1953125
  " class="svelte-j16aco"></polyline><g transform="translate(764.625124962866 348.4453125)"><polygon transform="rotate(96.5487532152125)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1423.94140625,130.25
      1123.2421875,155.25
  " class="svelte-j16aco"></polyline><g transform="translate(1188.765625 149.80241039764093)"><polygon transform="rotate(355.24738445178684)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg><svg class="svelte-j16aco"><polyline points="
      1423.94140625,130.25
      1310.7421875,489.1328125
  " class="svelte-j16aco"></polyline><g transform="translate(1331.6388367152294 422.8828125)"><polygon transform="rotate(287.5063750584245)" points="
      0,0
      12,6
      12,-6
  " class="svelte-j16aco"></polygon></g></svg> <div class="wrapper svelte-w5ultk" style="left: 1236.3051610375471px; top:422.88546972221445px"><div class="header svelte-w5ultk isTable"><div>  Chromosomes  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> chrom_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> chrom_name  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> chrom_seq  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> chrom_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> chrom_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 1563.984375px; top:219.38546972221445px"><div class="header svelte-w5ultk isTable"><div>  Flanking_seq  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> flank_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> flank_strand  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> up_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> up_stop  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> down_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> down_stop  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> gene_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 1549.59375px; top:446.23373086294623px"><div class="header svelte-w5ultk isTable"><div>  Intergenic_seq  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> igs_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> igs_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> igs_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 702.890625px; top:215.94824240695164px"><div class="header svelte-w5ultk isTable"><div>  Genes  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> gene_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> gene_strand  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> gene_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> gene_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 1057.7217613672212px; top:72.5px"><div class="header svelte-w5ultk isTable"><div>  Species  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> CommonName  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Family  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Genus  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Species  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Sex  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Mass  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> Lifespan  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 1354.8984375px; top:64px"><div class="header svelte-w5ultk isTable"><div>  Windows  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> wind_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> wind_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> wind_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> gene_count  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 875.3905517460489px; top:671.5px"><div class="header svelte-w5ultk isTable"><div>  Exons  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> exon_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> exon_strand  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> exon_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> exon_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> gene_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk" style="left: 1125px; top:674.2211127021563px"><div class="header svelte-w5ultk isTable"><div>  CDS  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> cds_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> cds_strand  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> cds_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> cds_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> gene_id  </span>        </div></div> </div><div class="wrapper svelte-w5ultk isSelectedTable" style="left: 660.7588994633502px; top:543px"><div class="header svelte-w5ultk isTable"><div>  Introns  </div> </div>  <div class="columns svelte-w5ultk"><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> intron_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> intron_strand  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> intron_seq_start  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-table-column svelte-1p2qnn1"></span> intron_seq_end  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> accession_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> chrom_id  </span>        </div><div class="line svelte-1s00ucb" draggable="false">  <span class="label svelte-1bc2dkx notNull"><span class="mdi mdi-key-link svelte-1p2qnn1"></span> gene_id  </span>        </div></div> <div class="selection-marker lt svelte-w5ultk"></div> <div class="selection-marker rt svelte-w5ultk"></div> <div class="selection-marker lb svelte-w5ultk"></div> <div class="selection-marker rb svelte-w5ultk"></div></div> </div>
  </body>
  
  </html>ploading sqlimg.html…]()



### Brief Description of Files
**numos.py** *(stands for ncbi updates macOS)*

- Checks NCBI (ncbi.nlm.nih.gov), using their command-line interface, for any new genomes that are not in the existing collection on our local computer. 
- If it finds new data, it checks for and handles duplicates, downloads the new data, then writes a CSV for easy-viewing and access to file paths.
- A text file is written with a log of each update, a record of changes, successes, and failures.
- An archive of the last metadata file you had before the update is saved.
- A text file 'data_to_upload.txt' with the list of data to be uploaded to MySQL is created to be used in the next class.

- Reads data_to_upload.txt, then accesses the file paths in the CSV with those accession numbers.
- Calculates and writes the data we need from the GFFs and FNAs to the MySQL database utilizing bulk inserts.

**dataframes.py**
- Takes information from MySQL to be further analyzed and/or graphed in python.

**window_variation.py**
- Used to determine most and least variable genomes by GC content amongst 100kb windows.
- **Data** folder was derived from this script for quick use in future analyses. Contains all of the genomes and chromosome IDs we used. 

# Analysis
### General Process
- Data is matched to its relatives with the established MySQL relationships, basic joins, and subqueries. Sub-sequences are 'cut' from the main chromosome sequence with the coordinates given in or calculated from the GFF.
- Stored procedures for various desired analyses assign variables, create temporary tables, and use loops to calculate GC content (Number of 'G' and 'C' per sequence  divided by the length of the sequence minus any 'N' content, which is 'unknown').
- Data is taken from temporary tables and queries and converted to Pandas dataframes for further analysis and visualization.

### Vizualization
This set of boxplots represents GC content for the intergenic sequences of the most variable and least variable genomes, respectively. Variability was determined by the average standard deviation for GC content per 100kb window (window_variation.py).
The sequences were put into 10 bins based on length. 
(The mean lines are included as dotted lines)

Modeled after this paper: https://pubmed.ncbi.nlm.nih.gov/21795750/
![Screenshot 2024-08-07 222537](https://github.com/user-attachments/assets/51b9030a-415b-4f84-98e6-a9c44d6deaf6)

![Screenshot 2024-08-07 222120](https://github.com/user-attachments/assets/48a83182-e993-4d84-88b1-ad855436d1fe)

This is a density plot for both genomes and their GC content by window. 
![image](https://github.com/user-attachments/assets/c7b58fde-22b9-4898-b2ea-ece9d6721c8f)


## Requirements and Assumptions for the script to run
- This version was written for MacOS High Sierra
- You must have the NCBI 'datasets' command-line interface downloaded and in your PATH. Instructions for adding to your PATH are under the 'Code' folder --> 'add_cli_to_PATH.txt'.
- You must have a local collection of genomes already downloaded on your computer. The package must be unzipped and rehydrated. The folder with the genomes must only have the genomes, the data catalog and metadata(renamed as <taxon>.jsonl) must be moved to the previous folder.
- This script was written for annotated genomes with the gff3 files. 
- This script was written for genomes with a chromosome-level assembly



## Changes that must be made to the script for it to run for you
- Open the script and adjust the paths indicated in the comment boxes before each class.
- Any deviations from the original purpose (different database design, different taxa, different genomes, no annotations, etc.) will require edits. 


# Issues
- Working with 'big data' like this was, and still is, a learning curve for optimization. Including all of the different sized windows we want drastically increases the upload time to something unreasonable. Downloading to a .csv for bulk insert isn't much faster.
- The GFF files we used are very heterogenous; this code was written specifically to tackle the issues we could see with our 20 genomes and may need changing for any expansions or change of taxon. Examples of these issues include:
  - Different naming conventions for the headers Ex:'assembly_info' vs 'assemblyInfo.'
  - Different parents among regions for the gffs, making it harder to connect exons to genes. Ex: An exon could have an 'mrna', 'gene', or 'ID' parent.
  - Different lengths and conventions of IDs.
  - Some have no names for the chromosomes, causing datatype mismatches in MySQL.
  - The data had no direct relation to the chromosome it belonged to besides ocurring after it in the file- this requires us to iterate line-by-line, which is slow.
  


# Future Work
- This code was written, to the best of my ability, with RAM and speed in mind. The program is still quite slow and I believe that the speed could be improved upon.
- Use BUSCO for annotations rather than the GFFs for more reliable and uniform data.
- Find a way to quickly get window information written to sql. Adding windows of 3kb, 10kb, 50kb, and 500kb exponentially raised the process time, so we only included the 100kb windows for now.
- Tying in with the previous point, find a way to do the initial bulk upload of data quickly and efficiently, possibly with a bulk insert.
- Fix small bug in class parse_upload() functions: igs, introns. Leaves small bits of invalid data that is insignificant to our analyses, but it would be nice to not have to delete them.
