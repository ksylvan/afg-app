'use client';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-blue-900 to-blue-800 text-white shadow-md">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-center space-y-4 md:space-y-2">
          <p className="text-center text-sm text-blue-100 md:text-base">
            © {currentYear} Alleluia Folk Group. All rights reserved.
          </p>
          <p className="text-center text-sm text-blue-200 md:text-base">
            Serving Holy Family Parish
          </p>
          <a
            href="mailto:info@alleluiafolkgroup.org"
            className="text-center text-sm font-medium text-amber-400 transition-colors duration-200 hover:text-amber-300 md:text-base"
          >
            info@alleluiafolkgroup.org
          </a>
        </div>
      </div>
    </footer>
  );
}
