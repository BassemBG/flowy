import { useState, useCallback } from "react";
import { Languages, Upload, FileText, Download, Loader2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

export default function Translation() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [extractedText, setExtractedText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const { toast } = useToast();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      processFile(droppedFile);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      processFile(selectedFile);
    }
  };

  const processFile = async (selectedFile: File) => {
    // Validate file type
    const allowedTypes = ["image/jpeg", "image/png", "image/jpg", "image/webp"];
    if (!allowedTypes.includes(selectedFile.type)) {
      toast({
        title: "Invalid file type",
        description: "Please upload an image file (JPG, PNG, WebP)",
        variant: "destructive",
      });
      return;
    }

    setFile(selectedFile);
    setIsProcessing(true);
    setExtractedText("");
    setTranslatedText("");

    try {
      // Call OCR API
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        "/api/automatic_translation/ocr/extract",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "OCR extraction failed");
      }

      const data = await response.json();
      const extracted = data.text || "";
      setExtractedText(extracted);

      toast({
        title: "Success",
        description: "Text extracted successfully from the image",
      });

      // Auto-translate after OCR
      await translateExtractedText(extracted);
    } catch (error) {
      console.error("OCR Error:", error);
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to extract text from image",
        variant: "destructive",
      });
      setFile(null);
    } finally {
      setIsProcessing(false);
    }
  };

  const translateExtractedText = async (textToTranslate: string) => {
    if (!textToTranslate.trim()) return;

    setIsTranslating(true);

    try {
      const response = await fetch(
        "/api/automatic_translation/translate",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: textToTranslate }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Translation failed");
      }

      const data = await response.json();
      setTranslatedText(data.translation || "");

      toast({
        title: "Success",
        description: "Text translated successfully",
      });
    } catch (error) {
      console.error("Translation Error:", error);
      toast({
        title: "Translation Error",
        description:
          error instanceof Error ? error.message : "Failed to translate text",
        variant: "destructive",
      });
    } finally {
      setIsTranslating(false);
    }
  };

  const handleDownload = (content: string, language: "arabic" | "french") => {
    if (!content) return;

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `document_${language}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast({
      title: "Downloaded",
      description: `${language === "arabic" ? "Arabic" : "French"} file downloaded successfully`,
    });
  };

  const clearFile = () => {
    setFile(null);
    setExtractedText("");
    setTranslatedText("");
    setIsProcessing(false);
    setIsTranslating(false);
  };

  return (
    <div className="page-container animate-fade-in">
      {/* Header */}
      <div className="page-header">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-xl gradient-brand flex items-center justify-center shadow-glow">
            <Languages className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="page-title">AI Document OCR</h1>
            <p className="page-description">
              Upload a scanned document image and extract text using AI-powered OCR
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Upload className="h-5 w-5 text-primary" />
              Upload Image
            </CardTitle>
          </CardHeader>
          <CardContent>
            {!file ? (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`
                  relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 cursor-pointer
                  ${isDragging
                    ? "border-primary bg-primary/5"
                    : "border-border hover:border-primary/50 hover:bg-muted/50"
                  }
                `}
              >
                <input
                  type="file"
                  onChange={handleFileSelect}
                  accept="image/jpeg,image/png,image/jpg,image/webp"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <div className="flex flex-col items-center gap-3">
                  <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
                    <Upload className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p className="text-lg font-medium text-foreground">
                      Drop your image here or click to browse
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Supports JPEG, PNG, WebP images
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg border border-border">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <FileText className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{file.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={clearFile}
                  disabled={isProcessing}
                  className="text-muted-foreground hover:text-destructive"
                >
                  <X className="h-5 w-5" />
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Processing Indicator - OCR */}
        {isProcessing && (
          <Card className="border-primary/20 bg-primary/5">
            <CardContent className="py-8">
              <div className="flex flex-col items-center gap-4">
                <div className="relative">
                  <div className="h-16 w-16 rounded-full bg-primary/20 flex items-center justify-center">
                    <Loader2 className="h-8 w-8 text-primary animate-spin" />
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-lg font-medium text-foreground">
                    Extracting text from image…
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Using AI OCR to process your document
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Processing Indicator - Translation */}
        {isTranslating && (
          <Card className="border-primary/20 bg-primary/5">
            <CardContent className="py-8">
              <div className="flex flex-col items-center gap-4">
                <div className="relative">
                  <div className="h-16 w-16 rounded-full bg-primary/20 flex items-center justify-center">
                    <Loader2 className="h-8 w-8 text-primary animate-spin" />
                  </div>
                </div>
                <div className="text-center">
                  <p className="text-lg font-medium text-foreground">
                    Translating to French…
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Using AI to translate your document
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Extracted Text Output */}
        {extractedText && !isProcessing && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <FileText className="h-5 w-5 text-primary" />
                Extracted Text (Arabic)
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="min-h-[300px] p-4 bg-muted/50 rounded-lg border border-border overflow-auto font-mono text-sm whitespace-pre-wrap break-words">
                {extractedText}
              </div>
              <p className="text-sm text-muted-foreground">
                Extracted Arabic text from your document (read-only)
              </p>
            </CardContent>
          </Card>
        )}

        {/* Translated Text Output */}
        {translatedText && !isTranslating && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Languages className="h-5 w-5 text-primary" />
                Translation (French)
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                value={translatedText}
                onChange={(e) => setTranslatedText(e.target.value)}
                className="min-h-[300px] font-mono text-sm resize-y"
                placeholder="French translation will appear here..."
              />
              <p className="text-sm text-muted-foreground">
                You can edit the translation above before downloading.
              </p>
            </CardContent>
          </Card>
        )}

        {/* Download Section */}
        {(extractedText || translatedText) && !isProcessing && !isTranslating && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="border-primary/20">
              <CardContent className="py-6">
                <div className="flex flex-col gap-4">
                  <div>
                    <p className="font-medium text-foreground">Arabic Text</p>
                    <p className="text-sm text-muted-foreground">
                      Download extracted Arabic
                    </p>
                  </div>
                  <Button
                    onClick={() => handleDownload(extractedText, "arabic")}
                    className="gradient-brand text-primary-foreground"
                    disabled={!extractedText}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Arabic
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card className="border-primary/20">
              <CardContent className="py-6">
                <div className="flex flex-col gap-4">
                  <div>
                    <p className="font-medium text-foreground">French Translation</p>
                    <p className="text-sm text-muted-foreground">
                      Download French translation
                    </p>
                  </div>
                  <Button
                    onClick={() => handleDownload(translatedText, "french")}
                    className="gradient-brand text-primary-foreground"
                    disabled={!translatedText}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download French
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
