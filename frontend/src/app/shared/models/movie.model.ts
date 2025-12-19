export interface Movie {
  id: string;
  title: string;
  year?: number;
  description?: string;
  posterUrl?: string;
}

export interface PlaybackInfo {
  manifestUrl: string;
}
