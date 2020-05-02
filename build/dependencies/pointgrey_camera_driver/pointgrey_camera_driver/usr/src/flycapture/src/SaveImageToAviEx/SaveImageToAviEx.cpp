//=============================================================================
// Copyright (c) 2001-2018 FLIR Systems, Inc. All Rights Reserved.
//
// This software is the confidential and proprietary information of FLIR
// Integrated Imaging Solutions, Inc. ("Confidential Information"). You
// shall not disclose such Confidential Information and shall use it only in
// accordance with the terms of the license agreement you entered into
// with FLIR Integrated Imaging Solutions, Inc. (FLIR).
//
// FLIR MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
// SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE, OR NON-INFRINGEMENT. FLIR SHALL NOT BE LIABLE FOR ANY DAMAGES
// SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
// THIS SOFTWARE OR ITS DERIVATIVES.
//============================================================================

#include "stdafx.h"

#include "FlyCapture2.h"
#include "FlyCapture2Video.h"
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace FlyCapture2;
using namespace std;

enum VideoType
{
	UNCOMPRESSED,
	MJPG,
	H264
};

void PrintBuildInfo()
{
	FC2Version fc2Version;
	Utilities::GetLibraryVersion(&fc2Version);

	ostringstream version;
	version << "FlyCapture2 library version: " << fc2Version.major << "."
		<< fc2Version.minor << "." << fc2Version.type << "."
		<< fc2Version.build;
	cout << version.str() << endl;

	ostringstream timeStamp;
	timeStamp << "Application build date: " << __DATE__ << " " << __TIME__;
	cout << timeStamp.str() << endl << endl;
}

void PrintCameraInfo(CameraInfo *pCamInfo)
{
	cout << endl;
	cout << "*** CAMERA INFORMATION ***" << endl;
	cout << "Serial number - " << pCamInfo->serialNumber << endl;
	cout << "Camera model - " << pCamInfo->modelName << endl;
	cout << "Camera vendor - " << pCamInfo->vendorName << endl;
	cout << "Sensor - " << pCamInfo->sensorInfo << endl;
	cout << "Resolution - " << pCamInfo->sensorResolution << endl;
	cout << "Firmware version - " << pCamInfo->firmwareVersion << endl;
	cout << "Firmware build time - " << pCamInfo->firmwareBuildTime << endl
		<< endl;
}

void PrintError(Error error) { error.PrintErrorTrace(); }

void SaveVideoHelper(VideoType VideoType,
	std::vector<Image> &vecImages,
	std::string videoFileName,
	float frameRate)
{
	Error error;
	FlyCapture2Video video;

	// Set maximum video file size to 2GB.
	// A new video file is generated when 2GB
	// limit is reached. Setting maximum file
	// size to 0 indicates no limit.
	const unsigned int k_videoFileSize = 2048;

	video.SetMaximumFileSize(k_videoFileSize);

	// Open the video file for appending images
	switch (VideoType)
	{
	case UNCOMPRESSED:
	{
		AVIOption option;
		option.frameRate = frameRate;
		error = video.Open(videoFileName.c_str(), &option);
	}
	break;
	case MJPG:
	{
		MJPGOption option;
		option.frameRate = frameRate;
		option.quality = 75;
		error = video.Open(videoFileName.c_str(), &option);
	}
	break;
	case H264:
	{
		H264Option option;
		option.frameRate = frameRate;
		option.bitrate = 1000000;
		option.height = vecImages[0].GetRows();
		option.width = vecImages[0].GetCols();
		error = video.Open(videoFileName.c_str(), &option);
	}
	break;
	}

	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return;
	}

	cout << endl;
	cout << "Appending " << vecImages.size()
		<< " images to video file: " << videoFileName.c_str() << endl;
	for (int imageCnt = 0; imageCnt < vecImages.size(); imageCnt++)
	{
		// Append the image to video file
		error = video.Append(&vecImages[imageCnt]);
		if (error != PGRERROR_OK)
		{
			PrintError(error);
			continue;
		}

		cout << "Appended image " << imageCnt << "..." << endl;
	}

	// Close the video file
	error = video.Close();
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return;
	}
}

int RunCamera(PGRGuid guid)
{
	const int k_numImages = 100;

	Error error;
	Camera cam;

	// Connect to a camera
	error = cam.Connect(&guid);
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	// Get the camera information
	CameraInfo camInfo;
	error = cam.GetCameraInfo(&camInfo);
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	PrintCameraInfo(&camInfo);

	// Start capturing images
	cout << "Starting capture... " << endl;
	error = cam.StartCapture();
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	std::vector<Image> vecImages;
	vecImages.resize(k_numImages);

	// Grab images
	Image rawImage;
	for (int imageCnt = 0; imageCnt < k_numImages; imageCnt++)
	{
		error = cam.RetrieveBuffer(&rawImage);
		if (error != PGRERROR_OK)
		{
			cout << "Error grabbing image " << imageCnt << endl;
			continue;
		}
		else
		{
			cout << "Grabbed image " << imageCnt << endl;
		}

		vecImages[imageCnt].DeepCopy(&rawImage);
	}

	// Stop capturing images
	cout << "Stopping capture... " << endl;
	error = cam.StopCapture();
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	// Check if the camera supports the FRAME_RATE property
	cout << "Detecting frame rate from camera... " << endl;
	PropertyInfo propInfo;
	propInfo.type = FRAME_RATE;
	error = cam.GetPropertyInfo(&propInfo);
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	float frameRateToUse = 15.0f;
	if (propInfo.present == true)
	{
		// Get the frame rate
		Property prop;
		prop.type = FRAME_RATE;
		error = cam.GetProperty(&prop);
		if (error != PGRERROR_OK)
		{
			PrintError(error);
		}
		else
		{
			// Set the frame rate.
			// Note that the actual recording frame rate may be slower,
			// depending on the bus speed and disk writing speed.
			frameRateToUse = prop.absValue;
		}
	}

	cout << "Using frame rate of " << fixed << setprecision(1) << frameRateToUse
		<< endl;

	// Uncompressed videos are always saved with avi containers with or without
	// extensions specified in the filepath
	ostringstream videoFileName;
	videoFileName << "SaveImageToAviEx-Uncompressed-" << camInfo.serialNumber;
	SaveVideoHelper(
		UNCOMPRESSED, vecImages, videoFileName.str().c_str(), frameRateToUse);

	// Motion JPEG videos are always saved with avi containers with or without
	// extensions specified in the filepath
	videoFileName.str("");
	videoFileName.clear();
	videoFileName << "SaveImageToAviEx-Mjpg-" << camInfo.serialNumber;
	SaveVideoHelper(MJPG, vecImages, videoFileName.str().c_str(), frameRateToUse);

	// H.264 videos defaults to saving in mp4 containers if extensions are not
	// specified. Otherwise the extension specified by the user will be used.
	videoFileName.str("");
	videoFileName.clear();
	videoFileName << "SaveImageToAviEx-H264-" << camInfo.serialNumber << ".mp4";
	SaveVideoHelper(H264, vecImages, videoFileName.str().c_str(), frameRateToUse);

	// Disconnect the camera
	error = cam.Disconnect();
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	return 0;
}

int main(int /*argc*/, char ** /*argv*/)
{
	PrintBuildInfo();

	Error error;

	// Since this application saves images in the current folder
	// we must ensure that we have permission to write to this folder.
	// If we do not have permission, fail right away.
	FILE *tempFile = fopen("test.txt", "w+");
	if (tempFile == NULL)
	{
		cout << "Failed to create file in current folder.  Please check "
			"permissions."
			<< endl;
		return -1;
	}
	fclose(tempFile);
	remove("test.txt");

	BusManager busMgr;
	unsigned int numCameras;
	error = busMgr.GetNumOfCameras(&numCameras);
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	if (numCameras < 1)
	{
		cout << "No camera detected." << endl;
		return -1;
	}
	else
	{
		cout << "Number of cameras detected: " << numCameras << endl;
	}

	PGRGuid guid;
	error = busMgr.GetCameraFromIndex(0, &guid);
	if (error != PGRERROR_OK)
	{
		PrintError(error);
		return -1;
	}

	cout << "Running the first camera." << endl;
	RunCamera(guid);

	cout << "Done! Press Enter to exit..." << endl;
	cin.ignore();

	return 0;
}
