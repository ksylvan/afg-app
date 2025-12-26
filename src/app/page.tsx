export default function Home() {
  return (
    <div className="min-h-screen">
      <section className="bg-gradient-to-br from-blue-900 via-blue-800 to-amber-600 px-4 py-20 text-center text-white md:py-32">
        <div className="container mx-auto">
          <h1 className="mb-4 text-4xl font-bold leading-tight md:text-6xl lg:text-7xl">
            Alleluia Folk Group
          </h1>
          <p className="mb-8 text-xl md:text-2xl lg:text-3xl text-blue-100">
            Serving Holy Family Parish through the gift of music
          </p>
          <p className="mb-6 max-w-2xl mx-auto text-lg md:text-xl text-blue-200">
            Join our community of 60+ musicians in creating prayerful, reverent, and joyous liturgical music.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#events" className="inline-block rounded-lg bg-amber-500 px-8 py-3 font-semibold text-blue-900 shadow-lg transition-colors hover:bg-amber-400">
              View Events
            </a>
            <a href="#join" className="inline-block rounded-lg border-2 border-white px-8 py-3 font-semibold text-white shadow-lg transition-colors hover:bg-white hover:text-blue-900">
              Join Our Ministry
            </a>
          </div>
        </div>
      </section>

      <main className="container mx-auto px-4 py-16 md:py-24">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="mb-6 text-4xl font-bold leading-tight text-blue-900 md:text-5xl lg:text-6xl">
            Welcome to Alleluia Folk Group
          </h1>
          <p className="mb-12 text-lg text-blue-800 md:text-xl">
            Serving Holy Family Parish through the gift of music
          </p>

          <div className="mx-auto mb-12 max-w-3xl rounded-lg border-l-4 border-amber-500 bg-blue-50 p-6 text-left shadow-md md:p-8">
            <h2 className="mb-3 text-2xl font-semibold text-blue-900">Our Mission</h2>
            <p className="leading-relaxed text-gray-800">
              To enhance the liturgical celebration at Holy Family Parish through music that
              inspires worship, fosters community, and draws all who participate deeper into
              the mystery of faith. We are dedicated to providing prayerful, reverent, and
              joyous music for Masses and special celebrations.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-3 text-xl font-semibold text-amber-600">Weekly Masses</h3>
              <p className="text-gray-700">
                We provide music for Sunday Masses throughout the year, creating a prayerful
                atmosphere for our parish community.
              </p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-3 text-xl font-semibold text-amber-600">Thursday Practices</h3>
              <p className="text-gray-700">
                Our dedicated musicians gather weekly for evening practices to prepare
                meaningful music for upcoming celebrations.
              </p>
            </div>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="mb-3 text-xl font-semibold text-amber-600">Special Events</h3>
              <p className="text-gray-700">
                We enrich Christmas, Easter, and other special liturgical celebrations with
                sacred and seasonal music.
              </p>
            </div>
          </div>

          <div className="mt-16 rounded-lg bg-gradient-to-r from-blue-900 to-blue-800 p-8 text-white shadow-lg md:p-12">
            <h2 className="mb-4 text-2xl font-bold md:text-3xl">Join Our Ministry</h2>
            <p className="mb-6 text-lg leading-relaxed text-blue-100">
              Whether you&apos;re a vocalist or instrumentalist, we welcome your gifts. Our group
              of 60+ members represents a wide range of musical backgrounds and experience
              levels, united by a shared love of liturgical music.
            </p>
            <p className="text-blue-200">
              Members coordinate schedules, sign up for events, and stay connected through
              our secure online system.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
