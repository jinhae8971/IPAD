# syntax=docker/dockerfile:1.7

###
# Frontend image — Vite build served by nginx.
#
# Stage 1 installs node_modules with npm ci and builds the SPA.
# Stage 2 is a tiny nginx that serves the static files and reverse
# proxies /api to the backend service.
###

FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY tsconfig.json tsconfig.app.json tsconfig.node.json vite.config.ts index.html ./
COPY src ./src

RUN npm run build


FROM nginx:1.27-alpine AS runtime

# Remove the default config that nginx ships with.
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/workstation.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
