from ninja import NinjaAPI, File
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema
from typing import List, Optional
from ninja.files import UploadedFile

api = NinjaAPI()


# @api.get("/test")
# def test(request):
#     return {"test": "success"}

@api.get("/tracks", response=List[TrackSchema])      # phản hồi lại class mình đã tạo ra 
def tracks(request, artist: Optional[str] = None):   # nếu không điền thì mặc định sẽ là None 
    if artist:                                        # nếu trong list có artist 
        return Track.objects.filter(artist__icontains=artist) # trả về những track có dữ liệu mà mình yêu cầu ( VD : http://localhost:8000/api/tracks?artist=a)
    return Track.objects.all()                         # trả về tất cả những dữ liệu mình đã sẵn có trong database 


@api.get("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema}) # gọi api với id mà mình muốn và phản hồi lại 
def track(request, track_id: int):                              
    try:                                                    # Bắt đầu block try-catch, thực hiện các câu lệnh trong block này và xử lý các ngoại lệ (exceptions) xảy ra
        track = Track.objects.get(pk=track_id)              # lấy đối tượng 'Track' từ  database dựa trên track_id. Đây là một phần của framework ORM(Object-Relational Mapping) truy vấn và tương tác với db
        return 200, track                                   # trả về mã trạng thái HTTP 200 và đối tượng 'track 'đã được lấy ra từ database
    except Track.DoesNotExist as e:                         # ngoại lệ xảy ( khi không tìm thấy track và track_id tương ứng nó sẽ bắt và gán vào biến e)
        return 404, {"message": "Track does not exist"}     # Trả về 404 và thông báo lỗi và một đối tượng json thông báo lỗi 'Track does not exist'


@api.post("/tracks", response={201: TrackSchema})           # là một API endpoint đăng ký cho phương thức POST trên đường dẫn , gửi yêu cầu POSt đến endpoint , thành công thì tạo mới 
def create(request, track: TrackSchema):                    # hàm với hai tham số là request yêu cầu gửi đến từ client và track là đối tượng kiểu dữ liệu TrackSchema đóng vai trò là dữ liệu đầu vào được truyền từ client
    track = Track.objects.create(**track.dict())            # tạo mới truyền toàn bộ thuộc tính của track vào phương thức create với (**track.dict())
    return track                                            # trả lại danh trách của track mới được tạo ra 


@api.put("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})  
def change_track(request, track_id : int , data:TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as e : 
        return 404 , {"message":"Could not find track"}

    



