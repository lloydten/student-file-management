from django.http import HttpResponse, JsonResponse
import dropbox
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
from django.template.loader import render_to_string

# Dopbox Credentials
client_id = 'sd3wsjb0wmgkjj0'
client_secret = 'gs5nt7vo3yqlqsj'
redirect_uri = 'http://localhost:8000/home'


def home(request):

        code = request.GET.get('code')
        
        # Exchanging the authorization code for an access token
        if code:

            # request.session.flush()
            client_id = 'sd3wsjb0wmgkjj0'
            client_secret = 'gs5nt7vo3yqlqsj'
            redirect_uri = 'http://localhost:8000/home'
            token_url = 'https://api.dropboxapi.com/oauth2/token'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {
                'code': code,
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
            }
            response = requests.post(token_url, headers=headers, data=data)
            response_data = response.json()
            print(response_data)
            
            try:
                if response_data['error'] =="invalid_grant":
                    dbx = dropbox.Dropbox(request.session['access_token'])
            except KeyError:
                
                # Saving the access token to session
            
                access_token = response_data.get('access_token')
                dbx = dropbox.Dropbox(access_token)
                request.session['access_token'] = access_token
            
          
        else:
           
            dbx = dropbox.Dropbox(request.session['access_token'])

        # List all files in Dropbox 
        result = dbx.files_list_folder('', recursive=True)
        num_items_in_result = len(result.entries) -1
        request.session['files_total'] = num_items_in_result
         
        files = []
        for entry in result.entries:
           
            if isinstance(entry, dropbox.files.FileMetadata):
                
                # Getting a temporary link to the file
                link = dbx.files_get_temporary_link(entry.path_display)
                preview_url = link.link

                # Adding file metadata and preview URL to the list
                files.append({
                    'name': entry.name,
                    'path_display': entry.path_display,
                    'size': entry.size,
                    'preview_url': preview_url,
                })

        # call  users_get_current_account method to get the current user's account info
        account_info = dbx.users_get_current_account()
        name = account_info.name.display_name
        formatted_name = ' '.join([word.capitalize() for word in name.split()])
       

        # Get user's profile picture URL
        account_info = dbx.users_get_current_account()
        profile_pic_url = account_info.profile_photo_url
        context={"files":files,"name":formatted_name,"files_total": num_items_in_result,'profile_pic':profile_pic_url}
        return render(request,'home.html',context)

def delete_file(request):
    if request.method == 'POST':

        dbx = dropbox.Dropbox(request.session['access_token'])
        
        file_path = request.POST.get('file_path')
        
        # Delete file from Dropbox
        dbx.files_delete(file_path)
    
    return redirect('home')


def upload_view(request):

    if request.method == 'POST':
        
        file = request.FILES.get('file')
        file_name = file.name
        file_size = file.size

        dbx = dropbox.Dropbox(request.session['access_token'])
     
        # Saving  uploaded file to Django's default storage
        file_path = default_storage.save(file_name, ContentFile(file.read()))

        # Uploading  file to Dropbox
        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), "/{}".format(file_name))

        # Deleting file from Django's default storage
        default_storage.delete(file_path)

        return redirect('home')

    return render(request, 'upload.html')

def download_file(request):
    if request.method == 'POST':

        file_path = request.POST.get('file_download')
        dbx = dropbox.Dropbox(request.session['access_token'])

        try:
            metadata, res = dbx.files_download(file_path)
            response = HttpResponse(res.content)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(metadata.name.encode('utf-8').decode('iso-8859-1'))
            return response
        except dropbox.exceptions.HttpError as err:
            print('Error downloading file: {}'.format(err))
    return HttpResponse('Invalid request method')

def images(request):

    dbx = dropbox.Dropbox(request.session['access_token'])

    images = []
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith(('.jpg', '.jpeg', '.png')):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
               
                images.append(link)
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")

    account_info = dbx.users_get_current_account()
    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']

    context = {'images': images,'name':formatted_name,'files_total':files_total}
    return render(request, 'images.html', context)

def videos(request):

    dbx = dropbox.Dropbox(request.session['access_token'])
    
    videos = []
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith(('.mp4', '.avi', '.mov')):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
                videos.append(link)
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")

    account_info = dbx.users_get_current_account()

    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']    

    context = {'videos': videos,"name":formatted_name,"files_total":files_total}
    return render(request, 'videos.html', context)


def audio(request):

    dbx = dropbox.Dropbox(request.session['access_token'])

    audio_files = []
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith(('.mp3', '.wav', '.m4a')):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
                audio_files.append(link)
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")

    account_info = dbx.users_get_current_account()
    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']
                           
    context = {'audio_files': audio_files,"name":formatted_name,'files_total':files_total}
    return render(request, 'audio.html', context)

def pdfs(request):

    dbx = dropbox.Dropbox(request.session['access_token'])

    pdfs = []
    name =[]
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith('.pdf'):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
                name.append(file.name)
                pdfs.append(file)
                
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")


    account_info = dbx.users_get_current_account()
    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']
                    
    context = {'pdfs': pdfs,'name':formatted_name,'files_total':files_total}
    return render(request, 'pdfs.html', context)


def text_files(request):

    dbx = dropbox.Dropbox(request.session['access_token'])

    texts = []
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith(('.txt','.csv')):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
                texts.append({'name': file.name, 'path': file.path_display, 'size': file.size, 'link': link})
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")

    account_info = dbx.users_get_current_account()
    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']  

    context = {'texts': texts,"name":formatted_name,'files_total':files_total}
    return render(request, 'text_files.html', context)


def code_files(request):

    dbx = dropbox.Dropbox(request.session['access_token'])

    files = []
    for file in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(file, dropbox.files.FileMetadata) and file.name.endswith(('.py','.java')):
            try:
                link = dbx.files_get_temporary_link(file.path_display).link
                files.append({'name': file.name, 'path': file.path_display, 'size': file.size, 'link': link})
            except dropbox.exceptions.ApiError as e:
                print("Error getting temporary link")

    account_info = dbx.users_get_current_account()
    name = account_info.name.display_name
    formatted_name = ' '.join([word.capitalize() for word in name.split()])
    files_total = request.session['files_total']  

    context = {'files': files,"name":formatted_name,'files_total':files_total}
    return render(request, 'code_files.html', context)

def search_dropbox(request,query):
 
    dbx = dbx = dropbox.Dropbox(request.session['access_token']) 
    
    # Searching for files matching the query
    search_results = dbx.files_search('', query).matches
    
    # Returning a list of FileMetadata objects for each file found
    return [result.metadata for result in search_results if isinstance(result.metadata, dropbox.files.FileMetadata)] 

def search(request):
    query = request.GET.get('query', '')
    results = search_dropbox(request,query)  
    
    # Rendering the template for each file found and append it to the search results
    file_cards = []
    for result in results:
        context = {'file': result, 'result': result}
        file_card = render_to_string('search_card.html', context=context)
        file_cards.append(file_card)
    
    # Returning the rendered HTML as part of the AJAX response
    response_data = {'file_cards': file_cards}
    return JsonResponse(response_data)

def authorize(request):
    
    request.session.flush()

    if request.method == "POST":
        client_id = 'sd3wsjb0wmgkjj0'
        client_secret = 'gs5nt7vo3yqlqsj'
        redirect_uri = 'http://localhost:8000/home'
        
        # Initiating the authorization flow
        auth_url = f'https://www.dropbox.com/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}'
        return redirect(auth_url)

    else:
        
        # Initiating the authorization flow
        client_id = 'sd3wsjb0wmgkjj0'
        redirect_uri = 'http://localhost:8000/home'
        auth_url = f'https://www.dropbox.com/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}'
        return redirect(auth_url)


def index(request):
    return render(request,'authorize.html')