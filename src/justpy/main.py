import justpy as jp

from wasabi import msg as Wmsg

from pipelines.extractive_summary import get_lsa_extractive_summary
from pipelines.abstractive_summary import get_summaries_from_hf_api

async def submit_text(self, msg):
    input_text = msg.form_data[0]['value']
    Wmsg.good(f"Received text: {input_text}")
    try:
        extractive_summary = get_lsa_extractive_summary(input_text, url=False)
        abstractive_summary = get_summaries_from_hf_api(extractive_summary)
    except Exception as e:
        Wmsg.warn(e)

    Wmsg.good(f"EXCTRACTIVE SUMMARY: {extractive_summary}")
    Wmsg.good(f"ABSTRACTIVE SUMMARY: {abstractive_summary}")

    Wmsg.good(f'Original len: {len(input_text)} - Summary len: {len(abstractive_summary)}')
    self.out.text = abstractive_summary

def summary_home():
    wp = jp.WebPage(debug=True)
    up_div = jp.Div(a=wp, classes='my-0 mx-auto max-w-3xl text-center')
    title = jp.H2(
        a=up_div, 
        text='AI Summarizer. Your personal AI assistent!', 
        classes='p-6 text-4xl font-bold italic')
    p = jp.P(
        a=up_div, 
        text="""Stop to waste your time for reading long (boring) text.
        Using this app, you can paste a text and get a summary version of it. 
        The summary version is provided, for you, by our AI algorithms.""", 
        classes='px-10 pb-10 text-center text-xl italic')
    
    down_left_div = jp.Div(
        a=wp, 
        classes='my-8 mx-auto max-w-3xl text-left')
    
    f = jp.Form(a=down_left_div)
    text_input_area = jp.Textarea(
        a=f,
        rows=8,
        cols=50,
        classes="""
        content-start flex-wrap whitespace-pre-wrap
        form-control
        font-normal
        text-gray-700
        bg-white bg-clip-padding
        border border-solid border-gray-300
        rounded
        transition
        ease-in-out
        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none""",
        placeholder='Paste some text ...',
        )

    summarizer_button = jp.Button(
        a=f,
        classes='px-3 py-2 text-white bg-blue-500 hover:bg-blue-700 white-text rounded',
        text='Summarize'
    )

    out1 = jp.A(
        a=down_left_div,
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
        text=''   
    )

    f.out = out1
    text_input_area.for_component = summarizer_button

    f.on('submit', submit_text)


    return wp

jp.justpy(summary_home, host='0.0.0.0', port=5010)


# import sys
# import logging
# logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
#                 level=logging.INFO, datefmt=None)
# logger = logging.getLogger("Summarizer")

# import justpy as jp

# from pipelines.extractive_summary import get_lsa_extractive_summary
# # from pipelines.abstractive_summary import get_summaries_from_hf_api

# input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
# p_classes = 'bg-gray-200 text-2xl font-bold border-2'
# h1_classes = "text-green-600 text-5xl font-bold"
# div_classes = "container text-center mx-4 space-y-2 px-4 bg-slate-300"
# button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
# input_classes = 'border m-2 p-2'

# inner_home_html = """
# <ul class="flex">
#   <li class="mr-6">
#     <a class="text-blue-500 hover:text-blue-80 rounded" href="/">Home</a>
#   </li>
#   <li class="mr-6">
#     <a class="text-blue-500 hover:text-blue-800 rounded" href="/services">Services</a>
#   </li>
#   <li class="mr-6">
#     <a class="text-blue-500 hover:text-blue-800 rounded" href="/teams">Teams</a>
#   </li>
#   <li class="mr-6">
#     <a class="text-blue-500 hover:text-blue-800 rounded" href="/contacts">Contacts</a>
#   </li>
# </ul>
# """

# def return_home_div():
#     return jp.Div(inner_html=inner_home_html)

# @jp.SetRoute('/services')
# def teams():
#     wp = jp.WebPage(title='AI Summarizer')
#     div = jp.Div(classes=div_classes, a=wp)
#     div.add(return_home_div())
#     div.add(jp.H1(classes=h1_classes, text='Our services'))
#     return wp

# @jp.SetRoute('/contacts')
# def teams():
#     wp = jp.WebPage(title='AI Summarizer')
#     div = jp.Div(classes=div_classes, a=wp)
#     div.add(return_home_div())
#     div.add(jp.H1(classes=h1_classes, text='Our contacts'))
#     return wp

# @jp.SetRoute('/teams')
# def teams():
#     wp = jp.WebPage(title='AI Summarizer')
#     div = jp.Div(classes=div_classes, a=wp)
#     div.add(return_home_div())
#     div.add(jp.H1(classes=h1_classes, text='Our teams'))
#     return wp


# async def submit_text(self, msg):
#   input_text = msg.form_data[0]['value']
#   logger.info(f"Received text: {input_text}")
#   extractive_summary = get_lsa_extractive_summary(input_text, url=False)
#   logger.info(f"EXCTRACTIVE SUMMARY: {extractive_summary}")
#   # abstractive_summary = get_summaries_from_hf_api(extractive_summary)
#   # logger.info(f"ABSTRACTIVE SUMMARY: {abstractive_summary}")
#   self.div.text = extractive_summary

# @jp.SetRoute('/')
# async def home(request):
#     wp = jp.WebPage(title='AI Summarizer')
#     wp.add(return_home_div())

#     main_div = jp.Div(a=wp, classes='w-full max-w-sm')
#     grid_div = jp.Div(a=main_div, classes='grid grid-rows-2 grid-flow-col gap-4')
#     row1 = jp.Div(classes='row-span-1 col-span-1 ...', a=grid_div)
#     row2 = jp.Div(classes='row-span-2 col-span-2 ...', a=grid_div)

#     form = jp.Form(a=row1, classes='w-full max-w-sm bg-gray-300 shadow-md rounded px-8 mb-2')
#     user_text_label = jp.Label(
#       text='Type some text', 
#       classes='form-label inline-block mb-2 text-gray-700', 
#       a=form)
#     in1 = jp.Input(
#       a=form,
#       type='text',
#       classes='form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
#       )
#     user_text_label.for_component = in1 # associate the label with the in1 component


#     form.div = jp.Div(
#       classes='block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4', 
#       a=row2)

#     output_label = jp.Label(
#       text='Your summary', 
#       classes='block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4', 
#       a=row2)

#     form.div = jp.Div(text='', a=row2, classes=div_classes)
#     form.on('submit', submit_text)
#     return wp

# jp.justpy(host='0.0.0.0', port=5010)