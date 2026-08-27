\# AI Media Generation API



\## 1. Project Overview



AI Media Generation is a FastAPI-based service for generating audio and visual media from scene-based scripts.



The system converts scene narration into speech, automatically selects an appropriate Tamil or English voice based on the narration and the user's selected gender, generates AI-based visuals from visual prompts, and combines the generated media into scene videos.



The project focuses on clean provider abstraction, API integration, media storage, error handling, testing, and connecting generated media to the overall workflow.



\---



\## 2. Objective



The objective of this project is to implement AI-generated audio and visual media required for video generation.



The system supports:



\- Text-to-Speech

\- Automatic language detection

\- Male/Female voice selection

\- Scene-wise narration

\- Audio generation

\- Audio preview

\- AI image generation

\- AI video generation

\- Scene-based visual generation

\- Local media storage

\- REST APIs

\- Provider abstraction

\- Error handling

\- Automated and manual tests



\---



\## 3. Expected Workflow



```text

Scene Script

\&#x20;   |

\&#x20;   +------> Text-to-Speech

\&#x20;   |             |

\&#x20;   |             v

\&#x20;   |          Voiceover

\&#x20;   |

\&#x20;   +------> Visual Prompt

\&#x20;                 |

\&#x20;                 v

\&#x20;           AI Image Generation

\&#x20;                 |

\&#x20;                 v

\&#x20;            Scene Image

\&#x20;                 |

\&#x20;                 +------> Audio

\&#x20;                 |

\&#x20;                 v

\&#x20;            Scene Video

\&#x20;                 |

\&#x20;                 v

\&#x20;            Scene Assets



4\\. Main Features

4.1 Text-to-Speech



The project uses Microsoft Edge TTS through the edge-tts Python package.



Narration text is converted into audio and stored as an MP3 file.



Example:



Narration

\&#x20;   |

\&#x20;   v

Edge TTS

\&#x20;   |

\&#x20;   v

scene\\\_1.mp3

4.2 Automatic Language Detection



The user does not need to manually select Tamil or English.



The system detects the language from the narration text.



Example:



விவசாயி தனது வயலில் வேலை செய்கிறார்.

\&#x20;               |

\&#x20;               v

\&#x20;             Tamil

A farmer is working in his field.

\&#x20;               |

\&#x20;               v

\&#x20;             English



The detected language is then used by the voice selector to choose the appropriate voice.



4.3 Voice Selection



The user selects only the gender:



Male



or:



Female



The system automatically selects the voice based on:



Detected narration language

Selected gender



Current voice mapping:



Language	Gender	Voice

Tamil	Female	ta-IN-PallaviNeural

Tamil	Male	ta-IN-ValluvarNeural

English	Female	en-US-AvaNeural

English	Male	en-US-AndrewNeural



Example:



Tamil + Female

\&#x20;     |

\&#x20;     v

ta-IN-PallaviNeural

Tamil + Male

\&#x20;     |

\&#x20;     v

ta-IN-ValluvarNeural

English + Female

\&#x20;     |

\&#x20;     v

en-US-AvaNeural

English + Male

\&#x20;     |

\&#x20;     v

en-US-AndrewNeural



The API user does not need to provide a technical voice ID.



5\\. Scene-wise Narration



Each scene contains its own narration.



Example:



{

\&#x20; "scene\\\_id": 1,

\&#x20; "narration": "A farmer is working in his field.",

\&#x20; "visual\\\_prompt": "A realistic farmer working in a green agricultural field.",

\&#x20; "voice": "male"

}



The narration is converted into audio specifically for that scene.



For multiple scenes:



Scene 1

\&#x20;   |

\&#x20;   +-- Narration

\&#x20;   +-- Voice

\&#x20;   +-- Audio

\&#x20;   +-- Image

\&#x20;   +-- Video





Scene 2

\&#x20;   |

\&#x20;   +-- Narration

\&#x20;   +-- Voice

\&#x20;   +-- Audio

\&#x20;   +-- Image

\&#x20;   +-- Video

6\\. AI Image Generation



The project integrates Hugging Face Inference Providers for AI image generation.



The image is generated from the scene's visual\\\_prompt.



Example workflow:



Visual Prompt

\&#x20;     |

\&#x20;     v

Hugging Face Image Generation

\&#x20;     |

\&#x20;     v

AI Generated Image



The image provider is separated behind an ImageProvider interface.



This allows another image provider to be integrated later without changing the core media-generation workflow.



7\\. AI Video Generation



The project uses a local video provider to create scene videos.



The generated image and generated audio are combined to create a scene video.



AI Image

\&#x20;   +

Voiceover Audio

\&#x20;   |

\&#x20;   v

Scene Video



The project does not attempt to build an AI video-generation model from scratch.



Instead, it integrates the required media-generation components through provider abstractions.



8\\. Scene-based Visual Generation



Each scene has a separate visual prompt.



Example:



Scene 1

\&#x20;   |

\&#x20;   +-- Narration

\&#x20;   |

\&#x20;   +-- Visual Prompt

\&#x20;            |

\&#x20;            v

\&#x20;       AI Image

\&#x20;            |

\&#x20;            v

\&#x20;       Scene Video



This allows different scenes to have different visual content.



9\\. Media Storage



Generated media is stored locally.



Project media structure:



media/

├── audio/

├── images/

└── videos/



Examples:



media/audio/scene\\\_1.mp3

media/images/scene\\\_1.png

media/videos/scene\\\_1.mp4

10\\. Audio Preview



Generated audio files are served through FastAPI's static media route.



Example:



http://127.0.0.1:8000/media/audio/scene\\\_1.mp3



The URL can be opened directly in a browser to listen to the generated narration.



A frontend can also use the returned audio URL with an HTML audio player:



<audio controls>

\&#x20;   <source

\&#x20;       src="http://127.0.0.1:8000/media/audio/scene\\\_1.mp3"

\&#x20;       type="audio/mpeg"

\&#x20;   >

</audio>



The project API returns both the audio file path and audio URL.



11\\. Project Architecture

app/

|

+-- api/

|   |

|   +-- routes/

|       +-- images.py

|       +-- projects.py

|       +-- scenes.py

|       +-- tts.py

|       +-- voices.py

|

+-- core/

|   +-- config.py

|

+-- providers/

|   |

|   +-- factory.py

|   |

|   +-- image/

|   |   +-- provider.py

|   |   +-- huggingface\\\_provider.py

|   |   +-- existing\\\_image\\\_provider.py

|   |

|   +-- tts/

|   |   +-- provider.py

|   |   +-- edge\\\_tts\\\_provider.py

|   |

|   +-- video/

|       +-- provider.py

|       +-- local\\\_video\\\_provider.py

|

+-- schemas/

|   +-- project.py

|   +-- scene.py

|   +-- tts.py

|

+-- services/

|   +-- media\\\_generation\\\_service.py

|   +-- project\\\_service.py

|   +-- scene\\\_service.py

|   +-- tts\\\_service.py

|   +-- voice\\\_selector.py

|

+-- storage/

|   +-- local\\\_storage.py

|

+-- main.py

12\\. Architecture Flow



The application follows a layered architecture:



Client

\&#x20; |

\&#x20; v

FastAPI Routes

\&#x20; |

\&#x20; v

Service Layer

\&#x20; |

\&#x20; +-------------------+

\&#x20; |                   |

\&#x20; v                   v

TTS Provider      Image Provider

\&#x20; |                   |

\&#x20; v                   v

Audio              Image

\&#x20; |                   |

\&#x20; +---------+---------+

\&#x20;           |

\&#x20;           v

\&#x20;     Video Provider

\&#x20;           |

\&#x20;           v

\&#x20;      Scene Video

\&#x20;           |

\&#x20;           v

\&#x20;     Local Storage

13\\. Provider Abstraction



The project uses provider interfaces so that external AI services can be replaced without rewriting the main application.



Image Provider

ImageProvider

\&#x20;   |

\&#x20;   +-- HuggingFaceImageProvider

\&#x20;   |

\&#x20;   +-- ExistingImageProvider

Text-to-Speech Provider

TTSProvider

\&#x20;   |

\&#x20;   +-- EdgeTTSProvider

Video Provider

VideoProvider

\&#x20;   |

\&#x20;   +-- LocalVideoProvider



The provider factory selects the provider based on configuration.



14\\. Provider Factory



The provider factory centralizes provider creation.



Example:



create\\\_tts\\\_provider()

create\\\_image\\\_provider()

create\\\_video\\\_provider()



The main services do not need to know how individual providers are initialized.



This improves:



Maintainability

Testability

Extensibility

Provider replacement

15\\. Configuration



Configuration is managed through environment variables.



Example .env:



IMAGE\\\_PROVIDER=huggingface

VIDEO\\\_PROVIDER=local

TTS\\\_PROVIDER=edge





HF\\\_TOKEN=your\\\_hugging\\\_face\\\_token





BASE\\\_URL=http://127.0.0.1:8000



Do not commit .env or API tokens to GitHub.



The project configuration is loaded using Pydantic Settings.



16\\. Installation

Step 1: Create a virtual environment

python -m venv venv

Step 2: Activate the virtual environment



PowerShell:



.\\\\venv\\\\Scripts\\\\Activate.ps1



If PowerShell blocks script execution:



Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned



Then activate the environment again:



.\\\\venv\\\\Scripts\\\\Activate.ps1

Step 3: Install dependencies

pip install -r requirements.txt

17\\. Environment Configuration



Create a .env file in the project root.



Example:



IMAGE\\\_PROVIDER=huggingface

VIDEO\\\_PROVIDER=local

TTS\\\_PROVIDER=edge





HF\\\_TOKEN=your\\\_hugging\\\_face\\\_token





BASE\\\_URL=http://127.0.0.1:8000



The Hugging Face token must be kept private.



Never hard-code the token inside Python source code.



18\\. Run the Application



Start the FastAPI application using:



uvicorn app.main:app --reload



The API will be available at:



http://127.0.0.1:8000



Swagger API documentation:



http://127.0.0.1:8000/docs

19\\. Health Check API



Endpoint:



GET /health



Example response:



{

\&#x20; "status": "healthy",

\&#x20; "service": "ai-media-generation",

\&#x20; "environment": "development"

}

20\\. Project Generation API



Endpoint:



POST /api/v1/projects/generate



This endpoint generates media for one or more scenes.



Request

{

\&#x20; "project\\\_id": "agriculture-demo-001",

\&#x20; "scenes": \\\[

\&#x20;   {

\&#x20;     "scene\\\_id": 1,

\&#x20;     "narration": "ஒரு விவசாயி தனது வயலில் வேலை செய்கிறார்.",

\&#x20;     "visual\\\_prompt": "A realistic farmer working in a green agricultural field during the morning, cinematic documentary style.",

\&#x20;     "voice": "female"

\&#x20;   }

\&#x20; ]

}

Processing Flow

API Request

\&#x20;   |

\&#x20;   v

Validate Request

\&#x20;   |

\&#x20;   v

Read Scene Narration

\&#x20;   |

\&#x20;   v

Detect Language

\&#x20;   |

\&#x20;   v

Select Male/Female Voice

\&#x20;   |

\&#x20;   v

Generate Audio

\&#x20;   |

\&#x20;   v

Generate Image

\&#x20;   |

\&#x20;   v

Generate Video

\&#x20;   |

\&#x20;   v

Store Scene Assets

\&#x20;   |

\&#x20;   v

Return Media URLs

Response

{

\&#x20; "project\\\_id": "agriculture-demo-001",

\&#x20; "scenes": \\\[

\&#x20;   {

\&#x20;     "scene\\\_id": 1,

\&#x20;     "audio\\\_path": "media/audio/scene\\\_1.mp3",

\&#x20;     "image\\\_path": "media/images/scene\\\_1.png",

\&#x20;     "video\\\_path": "media/videos/scene\\\_1.mp4",

\&#x20;     "audio\\\_url": "http://127.0.0.1:8000/media/audio/scene\\\_1.mp3",

\&#x20;     "image\\\_url": "http://127.0.0.1:8000/media/images/scene\\\_1.png",

\&#x20;     "video\\\_url": "http://127.0.0.1:8000/media/videos/scene\\\_1.mp4"

\&#x20;   }

\&#x20; ]

}

21\\. Scene Request Fields



Each scene contains:



Field	Description

scene\\\_id	Unique identifier for the scene

narration	Text that will be converted into speech

visual\\\_prompt	Prompt used for AI image generation

voice	User-selected gender: male or female



Example:



{

\&#x20; "scene\\\_id": 1,

\&#x20; "narration": "A farmer is working in his field.",

\&#x20; "visual\\\_prompt": "A realistic farmer working in a green field.",

\&#x20; "voice": "male"

}



The user does not need to provide the technical Edge TTS voice ID.



22\\. Audio URL



Generated audio is returned through:



audio\\\_url



Example:



http://127.0.0.1:8000/media/audio/scene\\\_1.mp3



This URL can be used by a frontend for audio preview.



23\\. Image URL



Generated images are returned through:



image\\\_url



Example:



http://127.0.0.1:8000/media/images/scene\\\_1.png

24\\. Video URL



Generated scene videos are returned through:



video\\\_url



Example:



http://127.0.0.1:8000/media/videos/scene\\\_1.mp4

25\\. API Media Serving



The application exposes the local media directory through FastAPI:



app.mount(

\&#x20;   "/media",

\&#x20;   StaticFiles(directory="media"),

\&#x20;   name="media",

)



This allows generated media to be accessed through HTTP URLs.



26\\. Voice Selection Test Results



The voice selector has been tested with Tamil and English narration.



Tamil Female

Narration:

விவசாயி தனது வயலில் வேலை செய்கிறார்.





Gender:

female





Detected language:

ta





Selected voice:

ta-IN-PallaviNeural

Tamil Male

Narration:

விவசாயி தனது வயலில் வேலை செய்கிறார்.





Gender:

male





Detected language:

ta





Selected voice:

ta-IN-ValluvarNeural

English Female

Narration:

A farmer is working in his field.





Gender:

female





Detected language:

en





Selected voice:

en-US-AvaNeural

English Male

Narration:

A farmer is working in his field.





Gender:

male





Detected language:

en





Selected voice:

en-US-AndrewNeural

27\\. Testing



The project includes tests for individual components and services.



Examples:



test\\\_tamil\\\_tts.py

test\\\_tamil\\\_action\\\_image.py

test\\\_voice\\\_selector.py

test\\\_media\\\_generation\\\_service.py

test\\\_project\\\_service.py

test\\\_multi\\\_scene.py

test\\\_project\\\_schema.py

test\\\_scene\\\_service.py

test\\\_tts\\\_provider.py

Python compilation check



Run:



python -m compileall .\\\\app



A successful result confirms that the application Python files compile without syntax errors.



Voice selector test



Run:



python test\\\_voice\\\_selector.py



The test verifies:



Tamil language detection

English language detection

Female voice selection

Male voice selection

28\\. Image Generation Test



The image generation provider can be tested independently.



Example:



python test\\\_tamil\\\_action\\\_image.py



The test generates an image from a visual prompt and stores it under the media directory.



29\\. Video Generation Test



The video pipeline can be tested using generated image and audio assets.



The pipeline combines:



Image

\&#x20;+

Audio

\&#x20;|

\&#x20;v

MP4 Video

30\\. Error Handling



The application includes error handling at provider, service, and API levels.



Important exceptions include:



MediaGenerationError

ProjectGenerationError

ProviderConfigurationError



Errors are converted into appropriate API responses.



Example:



{

\&#x20; "detail": "Failed to generate project 'project-id': ..."

}



Invalid request data is handled by FastAPI and Pydantic validation.



31\\. Provider Configuration Errors



If an unsupported provider is configured, the provider factory raises a configuration error.



Example:



Unsupported image provider: provider\\\_name



This prevents the application from silently using an incorrect provider.



32\\. API Validation



The project uses Pydantic schemas for request validation.



Examples of validation include:



Project ID must not be empty

Scene list must contain at least one scene

Scene ID must be at least 1

Narration must not be empty

Visual prompt must not be empty

Voice must not be empty



Invalid requests return FastAPI validation responses.



33\\. Security



API keys and access tokens are stored in environment variables.



Example:



HF\\\_TOKEN=...



Never commit secret credentials to source control.



The .env file should be included in .gitignore.



If a token is accidentally exposed, it should be revoked and replaced.



34\\. Optional Features



The following features are optional according to the project requirements:



Avatar generation

Talking avatar

Lip-sync



These features are not part of the required core implementation.



They can be added later as separate provider integrations.



35\\. Future Enhancements



Possible future improvements include:



Web-based frontend

Scene editor

Visual media preview

Audio preview UI

Video preview UI

Multiple image-provider support

Additional TTS providers

Cloud media storage

Background job processing

Generation progress tracking

Avatar generation

Talking avatar

Lip-sync

User authentication

Project history

36\\. Current Project Status

Required Deliverables

\&#x20;TTS integration

\&#x20;Voice selection

\&#x20;Scene-wise narration

\&#x20;Audio generation

\&#x20;Audio preview

\&#x20;AI image generation

\&#x20;AI video generation

\&#x20;Scene-based visual generation

\&#x20;Media storage

\&#x20;APIs

\&#x20;Provider abstraction

\&#x20;Error handling

\&#x20;Tests

\&#x20;Documentation

Optional Features

\&#x20;Avatar generation

\&#x20;Talking avatar

\&#x20;Lip-sync

37\\. Project Workflow Summary



The complete system works as follows:



User

\&#x20;|

\&#x20;| Project ID

\&#x20;| Scene narration

\&#x20;| Visual prompt

\&#x20;| Male/Female

\&#x20;|

\&#x20;v

FastAPI API

\&#x20;|

\&#x20;v

Project Service

\&#x20;|

\&#x20;+-------------------------+

\&#x20;|                         |

\&#x20;v                         v

Voice Selector         Visual Prompt

\&#x20;|                         |

\&#x20;v                         v

Language Detection      Image Provider

\&#x20;|                         |

\&#x20;v                         v

Voice Selection         AI Image

\&#x20;|                         |

\&#x20;v                         |

Edge TTS                  |

\&#x20;|                         |

\&#x20;v                         |

Audio --------------------+

\&#x20;          |

\&#x20;          v

\&#x20;     Video Provider

\&#x20;          |

\&#x20;          v

\&#x20;     Scene Video

\&#x20;          |

\&#x20;          v

\&#x20;     Local Storage

\&#x20;          |

\&#x20;          v

\&#x20;     API Response

\&#x20;          |

\&#x20;          +---- Audio URL

\&#x20;          +---- Image URL

\&#x20;          +---- Video URL

38\\. Design Principles



The implementation follows these principles:



Separation of Concerns



API routes, business logic, providers, schemas, and storage are separated.



Provider Abstraction



External AI providers are accessed through interfaces rather than being tightly coupled to business logic.



Reusability



Services can be reused for individual scenes or complete projects.



Error Handling



Provider and service failures are captured and returned through meaningful API errors.



Configuration-driven Providers



Providers can be selected through environment configuration.



Testability



Individual providers and services can be tested independently.



39\\. Technology Stack

Backend

Python

FastAPI

Uvicorn

Pydantic

Pydantic Settings

AI / Media

Edge TTS

Hugging Face Inference

AI image generation

Local video generation

Storage

Local file storage

API Documentation

FastAPI Swagger UI

OpenAPI

40\\. Running the Project - Quick Start

\\# Activate virtual environment

.\\\\venv\\\\Scripts\\\\Activate.ps1





\\# Install dependencies

pip install -r requirements.txt





\\# Start API

uvicorn app.main:app --reload



Open:



http://127.0.0.1:8000/docs

41\\. Example End-to-End Request

{

\&#x20; "project\\\_id": "agriculture-demo-001",

\&#x20; "scenes": \\\[

\&#x20;   {

\&#x20;     "scene\\\_id": 1,

\&#x20;     "narration": "ஒரு விவசாயி தனது வயலில் வேலை செய்கிறார்.",

\&#x20;     "visual\\\_prompt": "A realistic South Indian farmer working in a green agricultural field during the morning, cinematic documentary style.",

\&#x20;     "voice": "female"

\&#x20;   }

\&#x20; ]

}



Processing:



Tamil Narration

\&#x20;     |

\&#x20;     v

Language Detection

\&#x20;     |

\&#x20;     v

Tamil + Female

\&#x20;     |

\&#x20;     v

ta-IN-PallaviNeural

\&#x20;     |

\&#x20;     v

Audio Generation

\&#x20;     |

\&#x20;     v

AI Image Generation

\&#x20;     |

\&#x20;     v

Image + Audio

\&#x20;     |

\&#x20;     v

Scene Video

\&#x20;     |

\&#x20;     v

Media Storage

\&#x20;     |

\&#x20;     v

API Response

42\\. Conclusion



The AI Media Generation API provides a complete scene-based workflow for generating AI-assisted audio and visual media.



The implementation integrates:



Text-to-Speech

Automatic language detection

Male/Female voice selection

Scene-wise narration

Audio generation

Audio preview

AI image generation

AI video generation

Scene-based visual generation

Local media storage

REST APIs

Provider abstraction

Error handling

Testing








