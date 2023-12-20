
#Basado en: https://colab.research.google.com/github/WongKinYiu/yolov7/blob/main/tools/YOLOv7onnx.ipynb#scrollTo=ipHqto0J0kkq
import cv2
import random
import numpy as np
import onnxruntime as ort
import time

# ----- Funciones de entrada de datos ---------

def capture_stream():
	#capture = cv2.VideoCapture('/home/juancangaritan/yolov7/starling_test.mp4')
	capture = cv2.VideoCapture("rtspsrc location=rtsp://192.168.0.104:8900/live latency=150 ! decodebin ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1",cv2.CAP_GSTREAMER)
	return capture 

def get_frame(capture):
	success, img = capture.read()    
	time_ini = time.time()	
	return success, img

# ------ red neuronal --------

#---- Funciones display terminal ----
def salto_linea():
	print('\n')

def separador_punteado():
	print('------------------------')
#
#
#
# ------- Funciones de la red neuronal ----- 
#===================================================================================================================================================
#
# > Letterbox : Devuelve las dimensiones y el color de las cajas además de una capa con las cajas dibujadas (Solo para visualización)
#
#	Args:
#			> color: 	|	Color de fondo
#			> auto: 	|	Rectángulo más pequeño habilitado
#			> scaleup: 	|	Escalado de imagen (solo reduce para un mejo mapeo)
#			> stride:	|	Paso entre grupo de píxeles
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
def letterbox(img, new_shape=(640, 640),color=(114, 114, 114),auto=True, scaleup= True, stride = 32):
    im = img
    shape = im.shape[:2] #Forma actual [alto,ancho]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
    # ratio de escala(nuevo/viejo)
    r = min(new_shape[0]/shape[0], new_shape[1]/shape[1])
    #print(self.r)
    if not scaleup:
        r = min(r, 1.0)
    #padding
    new_unpad = int(round(shape[1]*r)),int(round(shape[0]*r))
    #print(new_unpad)
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    #print(self.dw)
    #print(self.dh)
    if auto:
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)    
    dw /= 2
    dh /= 2 #
    if shape[::-1] != new_unpad: 
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        #print(top)
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        #print('top = {} \n bottom = {} \n left = {} \n right = {}'.format(top,bottom,left,right))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return im, r, dw, dh

#=========================================================================================================================
#
# > process_output: Dibuja las cajas en la imagen en caso de existir alguna detección
#--------------------------------------------------------------------------------------------------------------------------
#
def process_output(outputs, ori_img, dw, dh, ratio):
	for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
		image = ori_img[int(batch_id)]
		#image = ori_img
		names = ['Aterrizaje_pad','Master_pad']
#
#		1. Dimensionando cajas
		dwdh = (dw, dh)
		box = np.array([x0, y0, x1, y1])
		box -= np.array(dwdh*2)
		box /= ratio
		box = box.round().astype(np.int32).tolist()
#
#		2. Etiqueta de objeto
		cls_id = int(cls_id)
#
#		3. Puntaje
		score = round(float(score),3)
#		
#		4. Posicionamiento de cajas y etiquetas en la imagen
		if cls_id == 0 and score >= 0.4:
			name = names[cls_id]
			color = [175,50,50]
			name += ' '+str(score)
			cv2.rectangle(image,tuple(box[:2]),tuple(box[2:]),[255,71,51],2)
			cv2.putText(image,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[255,71,51],thickness=2)
			overlay = image.copy()
			cv2.rectangle(overlay,tuple(box[:2]),tuple(box[2:]),[255,71,51],-1)
			cv2.addWeighted(overlay,0.3,image,1-0.3,0,image)
			cv2.imshow('Drone view', image)
		else: cv2.imshow('Drone view',image)
		if score < 0.4: 
			cv2.imshow('Drone view',image)
		return image
#
#		

#=========================================================================================================================
#
# > main: Función principal
#---------------------------------------------------------------------------------------------------------------------------
#
def main(img, session):
	
#	1. Cambio de color (opencv lee los canales rojo y azul invertidos)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#	2. Procesamiento de imagen para entregarla a la red 
	image = img.copy()
	image, ratio, dw, dh = letterbox(image, auto=False)
	image = image.transpose((2, 0, 1))
	image = np.expand_dims(image, 0)
	image = np.ascontiguousarray(image)
#
#	3. Normalizacion
	im = image.astype(np.float32)
	im /= 255
	im.shape
#
#	4. Obtener los identificadores de las capas de salida
	outname = [i.name for i in session.get_outputs()]
	outname
#
#	5. Obtener los identificadores de las capas de entrada
	inname = [i.name for i in session.get_inputs()]
	inname

	inp = {inname[0]:im}
#
#	6. Ejecucion
	outputs = session.run(outname, inp)[0]
	outputs 
#
#	7. Dibujar cajas en caso de que se detecten objetos
	ori_img = [img.copy()]
	img = process_output(outputs, ori_img, dw, dh, ratio)
		
#	
#
if __name__ == '__main__':
	#
	# 0. Inicio de variables -----------------------------------------------------------------------------------------------
	#
	#
	# 0.1. Red neuronal
	#
	cuda = True
	dnn_path = '/home/juancangaritan/yolov7/best_aterrizaje.onnx'
	providers = ['CUDAExecutionProvider' , 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
	session = ort.InferenceSession(dnn_path, providers = providers)
	# 1. Captura de video --------------------------------------------------------------------------------------------------
	#
	capture = capture_stream()
	#
	while (capture.isOpened()):
	#
	#   2. Captura de cada frame del video-------------------------------------------------------------------------------------
		sucess, img = get_frame(capture) #---> sucess: Se ha recibido un frame del stream ///// img: variable que contiene la imagen
	#
	#	3. Programa principal
		if sucess:
			main(img, session)
			if cv2.waitKey(1)&0xFF == ord('q'):
				break
	#   	
	#   

		if not sucess:
			print('[ERROR]: No hay fotogramas!')
			continue

		if cv2.waitKey(1)&0xFF == ord('q'):
			break
	capture.release()
	# 3. red neuronal ---------------------------------------------------


