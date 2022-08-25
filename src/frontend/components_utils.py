import justpy as jp

inner_home_html = """
<ul class="flex">
  <li class="mr-6">
    <a class="font-bold text-2xl text-black hover:text-gray-300 rounded" href="/">Home</a>
  </li>
  <li class="mr-6">
    <a class="font-bold text-2xl text-black hover:text-gray-300 rounded" href="/Services">Services</a>
  </li>
  <li class="mr-6">
    <a class="font-bold text-2xl text-black hover:text-gray-300 rounded" href="/Teams">Teams</a>
  </li>
  <li class="mr-6">
    <a class="font-bold text-2xl text-black hover:text-gray-300 rounded" href="/Contacts">Contacts</a>
  </li>
</ul>
"""

def return_home_div():
    return jp.Div(inner_html=inner_home_html)

def get_a_output_block(a):
    """Return a particular A html element, useful for showing long text"""
    return jp.A(
      a=a,
      text='',
      classes="""
      content-start flex-wrap whitespace-pre-wrap
      form-control
      font-normal
      text-gray-700
      bg-white bg-clip-padding
      border border-solid border-gray-300
      rounded-lg
      transition
      ease-in-out
      focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"""
      )

def get_block_div(a):
    """return a block box div"""
    div = jp.Div(a=a, classes='flex justify-center')
    div.add(jp.Div(classes='block p-6 rounded-lg shadow-ld bg-white max-w-sm'))
    return div

def get_form_block_card(a: jp.WebPage, on_submit=None, url=True, rows: int =8, cols: int =50, placeholder: str ='Paste some text ...') -> jp.Form:
    """return a form html element"""
    div_input_text = get_block_div(a=a)
    form = jp.Form(a=div_input_text, submit=on_submit)
    form.url = url
    input_text_area = jp.Textarea(
        a=form,
        rows=rows,
        cols=cols,
        classes="""
        content-start flex-wrap whitespace-pre-wrap
        form-control
        font-normal
        text-gray-700
        bg-white bg-clip-padding
        border border-solid border-gray-300
        rounded-lg
        transition
        ease-in-out
        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none""",
        placeholder=placeholder)
    b1 = jp.Button(
    a=form,
    classes='inline-block px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out',
    text='Summarize')
    # associate the textarea input to the button submit
    input_text_area.for_component = b1
    return form